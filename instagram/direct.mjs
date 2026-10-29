// Robô do direct do 3Tap: conversa sozinho com quem COMENTA um post ou RESPONDE um story.
// Pela API oficial o Instagram só deixa mandar direct para quem falou com a conta primeiro;
// então nunca escreve para quem só visualizou.
// Conversa:  1) "Oi! Você trabalha com o quê?"   2) depois da resposta, convida a seguir e se cadastrar.  Depois disso fica quieto
//            (a pessoa vira conversa normal para o Carlos responder).
// Roda como serviço sempre ligado (Railway). Variáveis:
//   IG_DM_TOKEN   token do Instagram com instagram_business_manage_messages e instagram_business_manage_comments
//   IG_APP_SECRET chave secreta do app da Meta (confere a assinatura de cada aviso)
//   IG_VERIFY     palavra qualquer, a mesma colocada no painel da Meta em Webhooks
//   IG_DM_ESTADO  arquivo onde guarda em que passo cada pessoa está (padrão direct-estado.json)
//   PORT          porta (o Railway define)
import { createServer } from "node:http";
import { createHmac, timingSafeEqual } from "node:crypto";
import { readFileSync, writeFileSync, existsSync } from "node:fs";

const API = "https://graph.instagram.com/v23.0";
let token = process.env.IG_DM_TOKEN;
const segredo = process.env.IG_APP_SECRET;
const verificar = process.env.IG_VERIFY;
const ARQ = process.env.IG_DM_ESTADO || "direct-estado.json";
const pessoas = existsSync(ARQ) ? JSON.parse(readFileSync(ARQ, "utf8")) : {};
const guardar = () => { try { writeFileSync(ARQ, JSON.stringify(pessoas)); } catch {} };

export const TEXTO = {
  pergunta: "Oi! Que bom te ver por aqui 😊 Você trabalha com o quê?",
  convite: "Que legal! Segue a gente e cadastra grátis no 3Tap: 3tapbrasil.com\nLá você vê quem está precisando do seu trabalho perto de você. Clicou, chegou! 🚀",
  respostaComentario: "Te chamei no direct! 😉",
};

async function api(path, corpo) {
  const r = await fetch(API + path, { method: "POST", headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" }, body: JSON.stringify(corpo) });
  const j = await r.json().catch(() => ({}));
  if (!r.ok || j.error) throw new Error(`${path}: ${JSON.stringify(j.error || j)}`);
  return j;
}
const direct = (para, texto) => api("/me/messages", { recipient: para, message: { text: texto } });

// Decide o que fazer com cada aviso da Meta. Devolve a lista de ações (útil para testar sem rede).
export function decidir(aviso, eu, estado = pessoas) {
  const acoes = [];
  for (const e of aviso.entry || []) {
    for (const m of e.messaging || []) {
      const quem = m.sender?.id, msg = m.message;
      if (!msg || msg.is_echo || !quem || quem === eu) continue;
      const passo = estado[quem]?.passo;
      if (!passo) { estado[quem] = { passo: "perguntou", em: Date.now() }; acoes.push({ tipo: "direct", para: { id: quem }, texto: TEXTO.pergunta }); }
      else if (passo === "perguntou") { estado[quem] = { passo: "convidou", em: Date.now(), profissao: (msg.text || "").slice(0, 80) }; acoes.push({ tipo: "direct", para: { id: quem }, texto: TEXTO.convite }); }
    }
    for (const c of e.changes || []) {
      const v = c.value || {};
      if (c.field !== "comments" || !v.id || !v.from?.id || v.from.id === eu || v.parent_id) continue;
      if (estado[v.from.id]) continue; // já está conversando com o robô
      estado[v.from.id] = { passo: "perguntou", em: Date.now() };
      acoes.push({ tipo: "direct", para: { comment_id: v.id }, texto: TEXTO.pergunta });
      acoes.push({ tipo: "resposta", comentario: v.id, texto: TEXTO.respostaComentario });
    }
  }
  return acoes;
}

async function executar(acoes) {
  for (const a of acoes) {
    try {
      if (a.tipo === "direct") await direct(a.para, a.texto);
      else await api(`/${a.comentario}/replies`, { message: a.texto });
      console.log("ok", a.tipo, JSON.stringify(a.para || a.comentario));
    } catch (e) { console.log("falhou", a.tipo, e.message); }
  }
}

function assinaturaOk(corpo, cabecalho) {
  if (!segredo) return true;
  const esperado = "sha256=" + createHmac("sha256", segredo).update(corpo).digest("hex");
  return Boolean(cabecalho) && cabecalho.length === esperado.length && timingSafeEqual(Buffer.from(cabecalho), Buffer.from(esperado));
}

async function renovar() {
  try {
    const u = new URL("https://graph.instagram.com/refresh_access_token");
    u.search = new URLSearchParams({ grant_type: "ig_refresh_token", access_token: token });
    const j = await (await fetch(u)).json();
    if (j.access_token) { token = j.access_token; console.log(`Token renovado, vale mais ${Math.round(j.expires_in / 86400)} dias`); }
  } catch (e) { console.log("Aviso: não renovou o token:", e.message); }
}

if (process.argv[1]?.endsWith("direct.mjs")) {
  if (!token) { console.error("Falta IG_DM_TOKEN"); process.exit(1); }
  const eu = (await (await fetch(`${API}/me?fields=user_id,username&access_token=${token}`)).json()).user_id;
  setInterval(renovar, 86400e3); // o token dura 60 dias; renovado todo dia enquanto o serviço vive
  createServer((req, res) => {
    const u = new URL(req.url, "http://x");
    if (req.method === "GET" && u.searchParams.get("hub.mode") === "subscribe") {
      const ok = verificar && u.searchParams.get("hub.verify_token") === verificar;
      res.writeHead(ok ? 200 : 403).end(ok ? u.searchParams.get("hub.challenge") : "");
      return;
    }
    if (req.method !== "POST") { res.writeHead(200).end("3Tap direct ok"); return; }
    let corpo = "";
    req.on("data", (d) => (corpo += d));
    req.on("end", () => {
      res.writeHead(200).end("ok"); // a Meta quer resposta rápida; o trabalho segue depois
      if (!assinaturaOk(corpo, req.headers["x-hub-signature-256"])) return console.log("assinatura inválida, ignorado");
      let aviso; try { aviso = JSON.parse(corpo); } catch { return; }
      const acoes = decidir(aviso, eu);
      if (acoes.length) { guardar(); executar(acoes); }
    });
  }).listen(process.env.PORT || 3000, () => console.log("Robô do direct ouvindo"));
}
