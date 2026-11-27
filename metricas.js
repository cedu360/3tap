// Contagem anônima de acesso (sem cookie, sem conta, sem IP guardado): telas abertas e toques em "Baixe o app".
// Vai para o painel do 3Tap só em números somados. Detalhes: https://app.3tapbrasil.com/cookies
(function () {
  try {
    var ua = navigator.userAgent || "";
    if (/bot|crawl|spider|slurp|lighthouse|preview|headless/i.test(ua) || !navigator.sendBeacon) return;
    var URL_ = "https://app.3tapbrasil.com/api/v1/metricas", KEY = "3tap:metrica", IDLE = 30 * 60 * 1000;
    var ios = /iPhone|iPad|iPod/.test(ua) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1), and = /Android/i.test(ua);
    var SRC = [[/chatgpt|openai/, "chatgpt"], [/gemini|bard/, "gemini"], [/perplexity/, "perplexity"], [/copilot/, "copilot"], [/google/, "google"], [/bing/, "bing"], [/duckduckgo/, "duckduckgo"], [/yahoo/, "yahoo"], [/instagram/, "instagram"], [/facebook|fb\.com|^fb$/, "facebook"], [/whatsapp|wa\.me/, "whatsapp"]];
    function clean(v) { return (v || "").toLowerCase().replace(/[^a-z0-9._-]/g, "").slice(0, 40) || null; }
    function source() {
      var q = new URLSearchParams(location.search), u = (q.get("utm_source") || "").toLowerCase(), h = "";
      try { h = document.referrer ? new URL(document.referrer).hostname.toLowerCase() : ""; } catch (e) {}
      var v = u || h;
      if (!v || h === location.hostname && !u) return null;
      for (var i = 0; i < SRC.length; i++) if (SRC[i][0].test(v)) return SRC[i][1];
      return clean(v.replace(/^www\./, ""));
    }
    function visit() {
      var v = null, now = Date.now();
      try { v = JSON.parse(sessionStorage.getItem(KEY) || "null"); } catch (e) {}
      if (!v || now - v.at > IDLE) v = { sid: (crypto.randomUUID ? crypto.randomUUID() : now + "-" + Math.random().toString(36).slice(2)), sent: false, source: source(), campaign: clean(new URLSearchParams(location.search).get("utm_campaign")) };
      v.at = now;
      return v;
    }
    function send(k, n) {
      var v = visit(), b = { surface: "site", sid: v.sid, events: [{ k: k, n: n }] };
      if (!v.sent) { b.source = v.source; b.campaign = v.campaign; }
      v.sent = true;
      try { sessionStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {}
      navigator.sendBeacon(URL_, new Blob([JSON.stringify(b)], { type: "text/plain" }));
    }
    send("v", location.pathname);
    // botões: Baixe o app (por aparelho) e os que levam ao app
    var CTA = { "app-store": "baixar-ios", "apk": "baixar-android", "encontrar": "abrir-app", "oferecer": "abrir-app", "agora": "abrir-app", "exemplo": "abrir-app", "busca": "abrir-app" };
    function name(cta) { return cta === "baixar-app" ? (ios ? "baixar-ios" : and ? "baixar-android" : "baixar-qr") : CTA[cta]; }
    document.addEventListener("click", function (e) { var a = e.target.closest && e.target.closest("[data-cta]"); if (a && a.tagName !== "FORM" && name(a.getAttribute("data-cta"))) send("c", name(a.getAttribute("data-cta"))); }, true);
    document.addEventListener("submit", function (e) { if (e.target.matches && e.target.matches("[data-cta]")) send("c", "abrir-app"); }, true);
  } catch (e) {}
})();
