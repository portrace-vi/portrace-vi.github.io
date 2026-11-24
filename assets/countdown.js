/* Cuenta regresiva a la fecha estimada (data-target). Sin JS se ve el número de días calculado al compilar. */
(function () {
  "use strict";
  var el = document.getElementById("cd");
  if (!el) return;
  var target = new Date(el.getAttribute("data-target")).getTime();
  if (isNaN(target)) return;
  var n = {};
  ["d", "h", "m", "s"].forEach(function (k) { n[k] = el.querySelector('[data-u="' + k + '"]'); });
  var passed = document.getElementById("cdp");
  function pad(v) { return v < 10 ? "0" + v : "" + v; }
  function set(d, h, m, s) { n.d.textContent = d; n.h.textContent = pad(h); n.m.textContent = pad(m); n.s.textContent = pad(s); }
  function tick() {
    var ms = target - Date.now();
    if (ms <= 0) { set(0, 0, 0, 0); if (passed) passed.hidden = false; return false; }
    var t = Math.floor(ms / 1000);
    set(Math.floor(t / 86400), Math.floor((t % 86400) / 3600), Math.floor((t % 3600) / 60), t % 60);
    return true;
  }
  if (tick()) { var id = setInterval(function () { if (!tick()) clearInterval(id); }, 1000); }
})();
