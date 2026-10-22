// Publica no Instagram do 3Tap pela API oficial. O token vem só da variável IG_TOKEN.
// Uso:  node publicar.mjs manha|tarde|noite [AAAA-MM-DD]   publica os itens daquele turno na fila.json
//       node publicar.mjs FEED|STORIES|REELS <arquivo> ["legenda"]   publica um item avulso
// Itens já publicados ficam em estado.json (IG_ESTADO) e nunca saem duas vezes.
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const API = "https://graph.instagram.com/v23.0";
const BASE = process.env.IG_BASE_IMAGENS || "https://3tapbrasil.com/instagram";
const token = process.env.IG_TOKEN;
if (!token) { console.error("Falta IG_TOKEN"); process.exit(1); }
const aqui = dirname(fileURLToPath(import.meta.url));
const ESTADO = process.env.IG_ESTADO || join(aqui, "estado.json");
const estado = existsSync(ESTADO) ? JSON.parse(readFileSync(ESTADO, "utf8")) : {};
const hojeBR = new Date(Date.now() - 3 * 3600e3).toISOString().slice(0, 10);
const espera = (ms) => new Promise((r) => setTimeout(r, ms));

async function api(path, params, method = "POST", base = API) {
  const url = new URL(base + path);
  for (const [k, v] of Object.entries({ ...params, access_token: token })) url.searchParams.set(k, v);
  const r = await fetch(url, { method });
  const j = await r.json();
  if (!r.ok || j.error) throw new Error(`${path}: ${JSON.stringify(j.error || j)}`);
  return j;
}

const [a, b, c] = process.argv.slice(2);
let itens;
if (["manha", "tarde", "noite"].includes(a)) {
  const dia = b || hojeBR;
  itens = JSON.parse(readFileSync(join(aqui, "fila.json"), "utf8")).filter((i) => i.dia === dia && i.turno === a);
} else if (["FEED", "STORIES", "REELS"].includes(a) && b) itens = [{ tipo: a, arquivo: b, legenda: c }];
else { console.error("Uso: node publicar.mjs manha|tarde|noite [dia]  ou  FEED|STORIES|REELS arquivo [legenda]"); process.exit(1); }
if (!itens.length) { console.log("Nada na fila para este turno."); process.exit(0); }

const eu = await api("/me", { fields: "user_id,username" }, "GET");
let n = 0;
for (const it of itens) {
  if (estado[it.arquivo]) { console.log(`Já publicado: ${it.arquivo}`); continue; }
  if (n++) await espera(4 * 60e3); // alguns minutos entre itens do mesmo turno
  const url = it.arquivo.startsWith("http") ? it.arquivo : `${BASE}/${it.arquivo}`;
  const p = { media_type: it.tipo === "FEED" ? undefined : it.tipo };
  if (it.tipo === "REELS") Object.assign(p, { video_url: url, share_to_feed: "true" }); else p.image_url = url;
  if (it.legenda && it.tipo !== "STORIES") p.caption = it.legenda;
  if (!p.media_type) delete p.media_type;
  const cont = await api(`/${eu.user_id}/media`, p);
  let ok = false;
  for (let i = 0; i < 60 && !ok; i++) {
    const s = await api(`/${cont.id}`, { fields: "status_code" }, "GET");
    if (s.status_code === "FINISHED") ok = true;
    else if (s.status_code === "ERROR") throw new Error(`Instagram recusou ${url}`);
    else await espera(5000);
  }
  if (!ok) throw new Error(`Tempo esgotado processando ${url}`);
  const pub = await api(`/${eu.user_id}/media_publish`, { creation_id: cont.id });
  estado[it.arquivo] = { id: pub.id, em: new Date().toISOString() };
  writeFileSync(ESTADO, JSON.stringify(estado, null, 1));
  console.log(`Publicado ${it.tipo} ${it.arquivo}: mídia ${pub.id}`);
}

try {
  const t = await api("/refresh_access_token", { grant_type: "ig_refresh_token" }, "GET", "https://graph.instagram.com");
  console.log(`Token renovado, vale mais ${Math.round(t.expires_in / 86400)} dias`);
} catch (e) { console.log("Aviso: não renovou o token:", e.message); }
