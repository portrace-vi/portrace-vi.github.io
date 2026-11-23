/* Efectos de interfaz. Todo es opcional: sin JS la página se ve completa. */
(function () {
  "use strict";
  var mq = function (q) { return window.matchMedia && window.matchMedia(q).matches; };
  var reduce = mq("(prefers-reduced-motion: reduce)");
  var fine = mq("(hover: hover) and (pointer: fine)");
  var $$ = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };

  /* barra de progreso + cabecera que se esconde al bajar */
  var bar = document.createElement("div"); bar.className = "progress"; document.body.appendChild(bar);
  var header = document.querySelector("header.top"), lastY = 0, ticking = false;
  function onScroll() {
    var y = window.scrollY, h = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0) + ")";
    if (header && !reduce) {
      if (y > lastY + 6 && y > 140) header.classList.add("hide");
      else if (y < lastY - 6 || y < 80) header.classList.remove("hide");
    }
    lastY = y; ticking = false;
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  /* aparición al hacer scroll, escalonada */
  if (!reduce && "IntersectionObserver" in window) {
    var sel = ".head,.card,.metric,.claim,.timeline li,.gantt,.box,.linklist li,.tablewrap,details,.answer,.edit-note,form.panel,.phone,.sub-h";
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    var seen = new Map();
    $$(sel).forEach(function (el) {
      if (el.closest(".hero")) return;
      var p = el.parentElement, n = seen.get(p) || 0; seen.set(p, n + 1);
      el.style.setProperty("--d", Math.min(n, 6) * 0.08 + "s");
      el.classList.add("rv"); io.observe(el);
    });
  }

  if (!fine || reduce) return;

  /* foco de luz que sigue al cursor dentro de tarjetas */
  document.addEventListener("pointermove", function (e) {
    var t = e.target.closest && e.target.closest(".card,.claim,.box,.linklist a");
    if (!t) return;
    var r = t.getBoundingClientRect();
    t.style.setProperty("--mx", (e.clientX - r.left) + "px");
    t.style.setProperty("--my", (e.clientY - r.top) + "px");
  }, { passive: true });

  /* botones magnéticos */
  $$(".btn").forEach(function (b) {
    b.addEventListener("pointermove", function (e) {
      var r = b.getBoundingClientRect();
      b.style.transform = "translate(" + ((e.clientX - r.left - r.width / 2) * 0.22) + "px," + ((e.clientY - r.top - r.height / 2) * 0.3) + "px)";
    });
    b.addEventListener("pointerleave", function () { b.style.transform = ""; });
  });

  /* resplandor que persigue al cursor en el hero */
  var hero = document.querySelector(".hero");
  if (hero) {
    var glow = document.createElement("div"); glow.className = "glow"; hero.appendChild(glow);
    var tx = 0, ty = 0, cx = 0, cy = 0, run = false;
    function loop() {
      cx += (tx - cx) * 0.12; cy += (ty - cy) * 0.12;
      glow.style.transform = "translate3d(" + cx + "px," + cy + "px,0) translate(-50%,-50%)";
      if (Math.abs(tx - cx) + Math.abs(ty - cy) > 0.5) requestAnimationFrame(loop); else run = false;
    }
    hero.addEventListener("pointermove", function (e) {
      var r = hero.getBoundingClientRect(); tx = e.clientX - r.left; ty = e.clientY - r.top;
      if (!run) { run = true; requestAnimationFrame(loop); }
    });
  }
})();
