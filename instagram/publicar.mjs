// Publica o post do dia no Instagram do 3Tap pela API oficial (Instagram API com login do Instagram).
// Uso: IG_TOKEN=... node publicar.mjs [n]   (sem n, escolhe o post pelo dia desde INICIO, em ciclo)
// O token fica só na variável de ambiente IG_TOKEN (segredo do ambiente), nunca em arquivo.
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const API = "https://graph.instagram.com/v23.0";
const BASE_IMAGENS = process.env.IG_BASE_IMAGENS || "https://3tapbrasil.com/instagram";
const INICIO = process.env.IG_INICIO || "2026-10-22"; // dia do post 1 (horário de Brasília)
const token = process.env.IG_TOKEN;
if (!token) { console.error("Falta IG_TOKEN"); process.exit(1); }

const aqui = dirname(fileURLToPath(import.meta.url));
const posts = JSON.parse(readFileSync(join(aqui, "legendas.json"), "utf8"));
const hojeBR = new Date(Date.now() - 3 * 3600e3).toISOString().slice(0, 10);
const dias = Math.round((Date.parse(hojeBR) - Date.parse(INICIO)) / 864e5);
const n = Number(process.argv[2]) || ((((dias % posts.length) + posts.length) % posts.length) + 1);
const post = { legenda: posts[n - 1], arquivo: `post-${String(n).padStart(2, "0")}.jpg` };

async function api(path, params, method = "POST", base = API) {
  const url = new URL(base + path);
  for (const [k, v] of Object.entries({ ...params, access_token: token })) url.searchParams.set(k, v);
  const r = await fetch(url, { method });
  const j = await r.json();
  if (!r.ok || j.error) throw new Error(`${path}: ${JSON.stringify(j.error || j)}`);
  return j;
}

const eu = await api("/me", { fields: "user_id,username" }, "GET");
// Nunca mais de um post por dia (evita parecer robô).
const ultimo = await api(`/${eu.user_id}/media`, { fields: "timestamp", limit: "1" }, "GET");
const ultimoDia = ultimo.data?.[0] && new Date(Date.parse(ultimo.data[0].timestamp.replace(/([+-]\d\d)(\d\d)$/, "$1:$2")) - 3 * 3600e3).toISOString().slice(0, 10);
if (ultimoDia === hojeBR && !process.argv[2]) { console.log("Já houve post hoje; nada a fazer."); process.exit(0); }
const imagem = `${BASE_IMAGENS}/${post.arquivo}`;
const c = await api(`/${eu.user_id}/media`, { image_url: imagem, caption: post.legenda });
for (let i = 0; i < 20; i++) {
  const s = await api(`/${c.id}`, { fields: "status_code" }, "GET");
  if (s.status_code === "FINISHED") break;
  if (s.status_code === "ERROR") throw new Error("Instagram recusou a imagem " + imagem);
  await new Promise((r) => setTimeout(r, 3000));
}
const pub = await api(`/${eu.user_id}/media_publish`, { creation_id: c.id });
console.log(`Publicado post ${n} em @${eu.username}: mídia ${pub.id}`);

// Renova o token (vale 60 dias; renovar estende o prazo).
try {
  const t = await api("/refresh_access_token", { grant_type: "ig_refresh_token" }, "GET", "https://graph.instagram.com");
  console.log(`Token renovado, vale mais ${Math.round(t.expires_in / 86400)} dias`);
} catch (e) { console.log("Aviso: não renovou o token:", e.message); }
