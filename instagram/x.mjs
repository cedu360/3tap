// Publica no X (Twitter) a mesma foto ou reel, pela API v2 com OAuth 1.0a.
// Só roda quando existem X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN e X_ACCESS_SECRET (segredos do repositório).
import { createHmac, randomBytes } from "node:crypto";
const { X_API_KEY: ck, X_API_SECRET: cs, X_ACCESS_TOKEN: at, X_ACCESS_SECRET: as } = process.env;
// Desligado por enquanto (a conta do X está sem crédito): para religar, ponha X_LIGADO: "1" no workflow.
export const xLigado = process.env.X_LIGADO === "1" && Boolean(ck && cs && at && as);
const API = "https://api.x.com/2";
const enc = (s) => encodeURIComponent(s).replace(/[!'()*]/g, (c) => "%" + c.charCodeAt(0).toString(16).toUpperCase());
const espera = (ms) => new Promise((r) => setTimeout(r, ms));

function assinatura(method, url) { // corpo JSON ou multipart não entra na assinatura
  const u = new URL(url), o = { oauth_consumer_key: ck, oauth_nonce: randomBytes(16).toString("hex"), oauth_signature_method: "HMAC-SHA1",
    oauth_timestamp: String(Math.floor(Date.now() / 1000)), oauth_token: at, oauth_version: "1.0" };
  const todos = [...Object.entries(o), ...u.searchParams.entries()].map(([k, v]) => [enc(k), enc(v)]).sort(([a, x], [b, y]) => (a < b ? -1 : a > b ? 1 : x < y ? -1 : 1));
  const base = [method, enc(u.origin + u.pathname), enc(todos.map(([k, v]) => `${k}=${v}`).join("&"))].join("&");
  o.oauth_signature = createHmac("sha1", `${enc(cs)}&${enc(as)}`).update(base).digest("base64");
  return "OAuth " + Object.entries(o).map(([k, v]) => `${enc(k)}="${enc(v)}"`).join(", ");
}
async function x(method, path, body) {
  const url = API + path, headers = { Authorization: assinatura(method, url) };
  if (body && !(body instanceof FormData)) { headers["Content-Type"] = "application/json"; body = JSON.stringify(body); }
  const r = await fetch(url, { method, headers, body });
  const t = await r.text(), j = t ? JSON.parse(t) : {};
  if (!r.ok) throw new Error(`X ${path}: ${r.status} ${t.slice(0, 300)}`);
  return j;
}
// Texto curto para o X: tira a linha do "link na bio" e põe o site
export function textoX(legenda = "") {
  const t = legenda.split("\n").filter((l) => !/link na bio/i.test(l)).join("\n").replace(/\n{3,}/g, "\n\n").trim();
  const fim = "\n\n👉 3tapbrasil.com";
  return (t.length + fim.length > 280 ? t.slice(0, 280 - fim.length - 1) + "…" : t) + fim;
}
export async function noX(it, bytes) {
  if (!xLigado || it.tipo === "STORIES") return null;
  const video = /\.(mp4|mov)$/i.test(it.arquivo);
  const ini = await x("POST", "/media/upload/initialize", { media_type: video ? "video/mp4" : "image/jpeg", total_bytes: bytes.length, media_category: video ? "tweet_video" : "tweet_image" });
  const id = ini.data.id, PEDACO = 4 * 1024 * 1024;
  for (let i = 0; i * PEDACO < bytes.length; i++) {
    const f = new FormData(); f.append("segment_index", String(i)); f.append("media", new Blob([bytes.subarray(i * PEDACO, (i + 1) * PEDACO)]));
    await x("POST", `/media/upload/${id}/append`, f);
  }
  let info = (await x("POST", `/media/upload/${id}/finalize`)).data?.processing_info;
  while (info && ["pending", "in_progress"].includes(info.state)) {
    await espera((info.check_after_secs || 5) * 1000);
    info = (await x("GET", `/media/upload?command=STATUS&media_id=${id}`)).data?.processing_info;
  }
  if (info?.state === "failed") throw new Error("X recusou o vídeo: " + JSON.stringify(info.error || info));
  return (await x("POST", "/tweets", { text: textoX(it.legenda), media: { media_ids: [id] } })).data.id;
}
