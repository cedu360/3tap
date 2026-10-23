// Pixel da Meta só com autorização (LGPD). Sem o ID, nada aparece e nada carrega.
(function () {
  var PIXEL_ID = "2889231331461207";
  var KEY = "3tap:ads-consent:v1";
  if (!PIXEL_ID) return;

  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  function loadPixel() {
    if (window.fbq) return;
    var f = window.fbq = window._fbq = function () { f.callMethod ? f.callMethod.apply(f, arguments) : f.queue.push(arguments); };
    f.push = f; f.loaded = true; f.version = "2.0"; f.queue = [];
    var s = document.createElement("script");
    s.async = true; s.src = "https://connect.facebook.net/en_US/fbevents.js";
    document.head.appendChild(s);
    f("init", PIXEL_ID);
    f("track", "PageView");
  }

  if (get() === "yes") return loadPixel();
  if (get() === "no") return;

  var box = document.createElement("aside");
  box.className = "consent";
  box.setAttribute("aria-label", "Preferências de privacidade");
  box.innerHTML =
    '<p><b>Sua privacidade</b><br>Se você aceitar, usamos o Pixel da Meta para mostrar o 3Tap no Instagram e no Facebook a quem visitou este site. ' +
    '<a href="https://3tap.up.railway.app/cookies">Detalhes</a></p>' +
    '<div><button type="button" class="btn btn-line" data-v="no">Recusar</button>' +
    '<button type="button" class="btn btn-primary" data-v="yes">Aceitar</button></div>';
  box.addEventListener("click", function (e) {
    var v = e.target && e.target.getAttribute && e.target.getAttribute("data-v");
    if (!v) return;
    set(v);
    box.remove();
    if (v === "yes") loadPixel();
  });
  document.body.appendChild(box);
})();
