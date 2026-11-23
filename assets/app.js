(function () {
  "use strict";
  var LANG = document.documentElement.lang === "es" ? "es" : "en";
  var T = window.STR[LANG], R = window.RACE;
  var $ = function (id) { return document.getElementById(id); };

  function h(tag, attrs, kids) {
    var e = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === "text") e.textContent = attrs[k]; else e.setAttribute(k, attrs[k]);
    });
    (kids || []).forEach(function (c) { if (c) e.appendChild(typeof c === "string" ? document.createTextNode(c) : c); });
    return e;
  }

  /* ---------- Tracker ---------- */
  var NF = LANG === "es" ? "es-ES" : "en-US";
  function nf(n) { try { return n.toLocaleString(NF, { useGrouping: "always" }); } catch (e) { return n.toLocaleString(NF); } }
  function score(p) {
    var w = R.weights, s = 0;
    Object.keys(p.status).forEach(function (k) { s += p.status[k] === "done" ? w[k] : p.status[k] === "wip" ? w[k] / 2 : 0; });
    return s;
  }
  function fmtDate(d) { return new Date(d + "T00:00:00Z").toLocaleDateString(NF, { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" }); }
  function ago(iso) {
    var s = Math.max(0, (Date.now() - new Date(iso).getTime()) / 1000);
    if (s < 90) return T.agoNow;
    var m = Math.round(s / 60); if (m < 60) return T.agoMin.replace("%n", m);
    var hr = Math.round(m / 60); if (hr < 48) return T.agoHour.replace("%n", hr);
    return T.agoDay.replace("%n", Math.round(hr / 24));
  }
  // Datos de GitHub: los trae el vigilante (tools/watch.py) cada 30 min y quedan en R.snapshot.
  // La web NO llama a GitHub desde el navegador: evita el límite de la API y no filtra la IP del visitante.
  function liveStats(p, el) {
    var s = (R.snapshot || {})[p.github];
    if (!s) return;
    if (s.unavailable) { el.textContent = T.unavailable; el.className += " gh-warn"; return; }
    var parts = ["★ " + nf(s.stars)];
    if (s.commits) parts.push(nf(s.commits) + " " + T.commitsWord);
    parts.push(T.pushed + " " + ago(s.pushed_at));
    el.textContent = parts.join(" · ");
    if (s.last_commit) el.appendChild(h("div", { "class": "gh-sub", text: T.lastCommit + ": “" + s.last_commit.message + "” · " + ago(s.last_commit.date) }));
    if (s.readme_baseline === false) el.appendChild(h("div", { "class": "gh-sub", text: T.readmeChanged + " " + ago(s.readme_changed_at) }));
  }

  function renderStats() {
    var playable = R.projects.filter(function (p) { return p.status.play === "done" && p.status.stable === "done"; }).length;
    var items = [
      [String(R.projects.length), T.projects],
      [playable ? String(playable) : "0", T.playable],
      [R.officialPC ? "✔" : T.none, T.official]
    ];
    var box = $("stats");
    items.forEach(function (it) { box.appendChild(h("div", { "class": "stat" }, [h("b", { text: it[0] }), h("span", { text: it[1] })])); });
  }

  function renderCards() {
    var EK = { readme: T.ekReadme, inferred: T.ekInferred, discord: T.ekDiscord, press: T.ekPress };
    var ranked = R.projects.slice().sort(function (a, b) { return score(b) - score(a); });
    var box = $("cards");
    ranked.forEach(function (p) {
      var sc = score(p), pbar = h("i", {});
      pbar.style.width = (sc * 10) + "%";
      var prog = h("div", { "class": "metric prog" }, [
        h("div", { "class": "m-top" }, [h("span", { text: T.score }), h("b", { text: sc.toFixed(1) + " / 10" })]),
        h("div", { "class": "m-bar" }, [pbar])
      ]);
      var ladder = h("ul", { "class": "ladder" }, R.milestones.map(function (m) {
        return h("li", {}, [h("i", { "class": "dot " + p.status[m.id] }), m[LANG]]);
      }));
      var metrics = null;
      if (p.metrics) {
        metrics = h("div", { "class": "metrics" }, p.metrics.map(function (m) {
          var pct = Math.round(m.done / m.total * 100), bar = h("i", {});
          bar.style.width = pct + "%";
          return h("div", { "class": "metric" }, [
            h("div", { "class": "m-top" }, [h("span", { text: m.label[LANG] }), h("b", { text: nf(m.done) + " / " + nf(m.total) + " · " + pct + "%" })]),
            h("div", { "class": "m-bar" }, [bar])
          ]);
        }));
      }
      var evidence = h("details", { "class": "evidence" }, [
        h("summary", { text: T.evidence + " (" + p.evidence.length + ")" }),
        h("ul", {}, p.evidence.map(function (e) {
          var li = h("li", {}, [h("span", { "class": "ek ek-" + e.kind, text: EK[e.kind] }), " " + e.text[LANG]]);
          if (e.url) { li.appendChild(document.createTextNode(" ")); li.appendChild(h("a", { href: e.url, rel: "noopener nofollow", target: "_blank", text: "↗" })); }
          return li;
        }))
      ]);
      var links = h("div", { "class": "links" });
      if (p.url) {
        [[p.url, T.repo], [p.url + "/commits", T.commits], [p.url + "/issues", T.issues]].concat(p.discord ? [[p.discord, "Discord"]] : []).forEach(function (l) {
          links.appendChild(h("a", { href: l[0], rel: "noopener nofollow", target: "_blank", text: l[1] + " ↗" }));
        });
      } else links.appendChild(h("span", { "class": "pending", text: T.repoPending }));
      var gh = h("div", { "class": "gh" });
      box.appendChild(h("article", { "class": "card" }, [
        h("h3", {}, [p.name, h("span", { "class": "by", text: T.by + " " + p.author })]),
        gh,
        prog,
        h("p", { "class": "hl", text: p.highlight[LANG] }),
        h("p", { text: p.approach[LANG] }),
        ladder,
        metrics,
        h("p", { "class": "note", text: p.note[LANG] }),
        evidence,
        h("p", { "class": "checked", text: T.checked + ": " + fmtDate(p.checked.date) + " · " + p.checked.against[LANG] }),
        links
      ]));
      liveStats(p, gh);
    });
    $("meta").textContent = T.updated + ": " + fmtDate(R.updated) + "." + (R.snapshotAt ? " " + T.watcher + " " + ago(R.snapshotAt) + "." : "");
  }

  /* ---------- GPU table: [regex, label, relative score (Xbox Series X ≈ 100), VRAM GB] ---------- */
  var GPUS = window.GPUS_RAW.map(function (g) { return { re: new RegExp(g.re, "i"), label: g.label, score: g.score, vram: g.vram, slug: g.slug }; });

  var VRAMS = [2, 4, 6, 8, 10, 12, 16, 20, 24, 32];
  var RAMS = [8, 16, 32, 64, 128];
  var THREADS = [4, 6, 8, 12, 16, 24, 32];
  var CPU_LIST = window.CPUS_RAW; // [{brand,label,threads,score}] Ryzen 7 3700X ≈ Xbox Series X ≈ 100

  var detected = { gpuIdx: -1, laptop: false, apple: false, mobile: /Android|iPhone|iPad|Mobile/i.test(navigator.userAgent) };

  function detectGPU() {
    try {
      var c = document.createElement("canvas");
      var gl = c.getContext("webgl") || c.getContext("experimental-webgl");
      if (!gl) return "";
      var ext = gl.getExtension("WEBGL_debug_renderer_info");
      return ext ? String(gl.getParameter(ext.UNMASKED_RENDERER_WEBGL)) : "";
    } catch (e) { return ""; }
  }
  var rendererStr = detectGPU();
  if (rendererStr) {
    detected.apple = /apple/i.test(rendererStr);
    detected.laptop = /laptop|max-q|mobile/i.test(rendererStr);
    for (var i = 0; i < GPUS.length; i++) if (GPUS[i].re.test(rendererStr)) { detected.gpuIdx = i; break; }
  }

  function opt(v, t, sel) { var o = h("option", { value: v, text: t }); if (sel) o.selected = true; return o; }
  function nearest(list, n) { return list.reduce(function (a, b) { return Math.abs(b - n) < Math.abs(a - n) ? b : a; }); }

  var gpuSel = $("gpu"), vramSel = $("vram"), ramSel = $("ram"), cpuSel = $("cpu"), threadsSel = $("threads"), stSel = $("storage");
  var vramTouched = false;

  function buildForm() {
    gpuSel.appendChild(opt("", T.pickGpu));
    GPUS.forEach(function (g, i) { gpuSel.appendChild(opt(String(i), g.label, i === detected.gpuIdx)); });
    gpuSel.appendChild(opt("other", T.unknownGpu));
    VRAMS.forEach(function (v) { vramSel.appendChild(opt(String(v), v + " " + T.gb, v === 8)); });
    var dm = navigator.deviceMemory;
    RAMS.forEach(function (v) { ramSel.appendChild(opt(String(v), v + " " + T.gb, v === 16)); });
    var ht = navigator.hardwareConcurrency || 0;
    // CPU por modelo (los navegadores no pueden leerlo); hilos solo como plan B
    cpuSel.appendChild(opt("", T.cpuUnknown, true));
    ["Intel", "AMD"].forEach(function (brand) {
      var grp = h("optgroup", { label: brand });
      CPU_LIST.forEach(function (c, i) { if (c.brand === brand) grp.appendChild(opt(String(i), c.label)); });
      cpuSel.appendChild(grp);
    });
    THREADS.forEach(function (v) { threadsSel.appendChild(opt(String(v), v + (v === 32 ? "+" : ""), ht ? v === nearest(THREADS, ht) : v === 8)); });
    $("threadsLabel").hidden = false;
    [["hdd", T.hdd], ["sata", T.sata], ["nvme", T.nvme]].forEach(function (s) { stSel.appendChild(opt(s[0], s[1], s[0] === "nvme")); });

    // hints
    var notes = [];
    if (detected.gpuIdx >= 0) { $("gpuHint").textContent = T.autodetected + GPUS[detected.gpuIdx].label; }
    else $("gpuHint").textContent = T.notDetected;
    if (detected.laptop) notes.push(T.laptopNote);
    if (detected.apple) notes.push(T.appleNote);
    if (detected.mobile) notes.push(T.mobileNote);
    if (notes.length) $("gpuHint").textContent += " " + notes.join(" ");
    if (dm) $("ramHint").textContent = dm >= 8 ? T.browserCap : T.autodetected + dm + " " + T.gb;
    $("cpuHint").textContent = T.cpuHintBrowser;
    if (detected.gpuIdx >= 0) syncVram();
  }

  function syncVram() {
    var g = GPUS[+gpuSel.value];
    if (!g || vramTouched) return;
    var v = g.vram;
    if (detected.laptop && +gpuSel.value === detected.gpuIdx) v = Math.min(v, 8);
    vramSel.value = String(nearest(VRAMS, v));
  }

  /* ---------- Scoring ---------- */
  function lvl(v, cuts) { var l = 0; cuts.forEach(function (c, i) { if (v >= c) l = i + 1; }); return l; }
  // cuts = thresholds for level 1,2,3,4
  function evaluate() {
    if (gpuSel.value === "") return null;
    var score;
    if (gpuSel.value === "other") score = 40;
    else {
      score = GPUS[+gpuSel.value].score;
      if (detected.laptop && +gpuSel.value === detected.gpuIdx) score *= 0.75;
    }
    var vram = +vramSel.value, ram = +ramSel.value, st = stSel.value;
    var cpuComp;
    if (cpuSel.value === "") {
      var th = +threadsSel.value;
      cpuComp = { key: "rowCpu", level: lvl(th, [6, 12, 16, 24]), val: th + (th === 32 ? "+" : "") + " " + T.threadsWord };
    } else {
      var cm = CPU_LIST[+cpuSel.value];
      cpuComp = { key: "rowCpu", level: lvl(cm.score, [70, 95, 150, 210]), val: cm.label };
    }
    var comps = [
      { key: "rowGpu", level: lvl(score, [50, 95, 150, 250]), val: Math.round(score) + " pts" },
      { key: "rowVram", level: lvl(vram, [6, 10, 16, 24]) , val: vram + " " + T.gb },
      { key: "rowRam", level: ({ 8: 0, 16: 2, 32: 3, 64: 4, 128: 4 })[ram], val: ram + " " + T.gb },
      cpuComp,
      { key: "rowStorage", level: ({ hdd: 0, sata: 2, nvme: 4 })[st], val: ({ hdd: T.hdd, sata: T.sata, nvme: T.nvme })[st] }
    ];
    var min = comps.reduce(function (a, c) { return Math.min(a, c.level); }, 4);
    var worst = comps.filter(function (c) { return c.level === min; })[0];
    return { comps: comps, overall: min, worst: worst };
  }

  var last = null;
  function render() {
    var box = $("result"); box.textContent = "";
    last = evaluate();
    if (!last) { box.appendChild(h("div", { "class": "empty", text: T.pickPrompt })); return; }
    var o = last.overall;
    var meter = h("div", { "class": "meter" }, [1, 2, 3, 4].map(function (n) { return h("i", { "class": n <= o ? "on" : "" }); }));
    box.appendChild(h("div", { "class": "res-top" }, [
      h("span", { "class": "label", text: T.yourVerdict }),
      h("h3", { text: T.verdict[o] }),
      h("p", { text: T.verdictDesc[o] }),
      meter
    ]));
    var rows = h("div", { "class": "rows" }, last.comps.map(function (c) {
      return h("div", { "class": "row" }, [
        h("div", {}, [h("b", { text: T[c.key] }), c.val]),
        h("span", { "class": "tag t" + c.level, text: T.tag[c.level] })
      ]);
    }));
    box.appendChild(rows);
    box.appendChild(h("p", { "class": "bottle", text: o >= 4 ? T.noBottleneck : T.bottleneck.replace("%c", T[last.worst.key]) }));
    var share = h("div", { "class": "share" }, [
      h("button", { "class": "btn sec", type: "button", id: "copyBtn", text: T.copyBtn }),
      h("button", { "class": "btn pri", type: "button", id: "imgBtn", text: T.imgBtn })
    ]);
    if (navigator.share) share.appendChild(h("button", { "class": "btn sec", type: "button", id: "shareBtn", text: T.shareBtn }));
    box.appendChild(share);
    $("copyBtn").onclick = copyResult; $("imgBtn").onclick = downloadCard;
    if ($("shareBtn")) $("shareBtn").onclick = function () { try { navigator.share({ text: shareText(), url: location.href }); } catch (e) {} };
  }

  function shareText() { return T.shareText.replace("%v", T.verdict[last.overall]) + " " + location.href; }
  function copyResult() {
    var b = $("copyBtn");
    function ok() { var t = b.textContent; b.textContent = T.copied; setTimeout(function () { b.textContent = t; }, 1600); }
    try { navigator.clipboard.writeText(shareText()).then(ok, function () {}); } catch (e) {}
  }

  function downloadCard() {
    var W = 1200, H = 630, c = document.createElement("canvas"); c.width = W; c.height = H;
    var x = c.getContext("2d");
    x.fillStyle = "#0a0a0f"; x.fillRect(0, 0, W, H);
    function orb(cx, cy, r, col, al) {
      var g = x.createRadialGradient(cx, cy, 0, cx, cy, r);
      g.addColorStop(0, col.replace("A", al)); g.addColorStop(1, col.replace("A", 0));
      x.fillStyle = g; x.fillRect(0, 0, W, H);
    }
    orb(1020, 90, 520, "rgba(255,79,139,A)", .55); orb(1120, 520, 480, "rgba(255,154,90,A)", .35);
    x.strokeStyle = "rgba(255,255,255,.10)"; x.lineWidth = 1.5;
    [260, 420, 600].forEach(function (r) { x.beginPath(); x.arc(1010, 330, r, 0, 7); x.stroke(); });
    x.textBaseline = "alphabetic";
    x.fillStyle = "#9a9aab"; x.font = "500 26px Inter,Arial,sans-serif";
    x.fillText(T.cardSub, 80, 110);
    x.fillStyle = "#f4f4f7"; x.font = "700 40px 'Space Grotesk',Arial,sans-serif";
    x.fillText("PortRace VI", 80, 170);
    var vg = x.createLinearGradient(80, 0, 700, 0); vg.addColorStop(0, "#ff4f8b"); vg.addColorStop(1, "#ff9a5a");
    x.fillStyle = vg; x.font = "700 128px 'Space Grotesk',Arial,sans-serif";
    x.fillText(T.verdict[last.overall], 80, 370);
    x.fillStyle = "#f4f4f7"; x.font = "500 34px Inter,Arial,sans-serif";
    var name = gpuSel.value === "other" ? T.unknownGpu : GPUS[+gpuSel.value].label;
    x.fillText(name + " · " + ramSel.value + " " + T.gb + " RAM", 80, 450);
    x.fillStyle = "#9a9aab"; x.font = "500 26px Inter,Arial,sans-serif";
    x.fillText(location.host || "portrace.vi", 80, 560);
    var a = document.createElement("a"); a.download = "portrace-vi-result.png"; a.href = c.toDataURL("image/png"); a.click();
  }

  /* ---------- init ---------- */
  renderStats(); renderCards(); buildForm();
  try {
    var q = new URLSearchParams(location.search).get("gpu");
    if (q) for (var k = 0; k < GPUS.length; k++) if (GPUS[k].slug === q) { gpuSel.value = String(k); $("gpuHint").textContent = ""; syncVram(); }
  } catch (e) {}
  render();
  gpuSel.addEventListener("change", function () {
    vramTouched = false; syncVram();
    if (+gpuSel.value !== detected.gpuIdx || gpuSel.value === "") $("gpuHint").textContent = "";
    render();
  });
  vramSel.addEventListener("change", function () { vramTouched = true; render(); });
  cpuSel.addEventListener("change", function () { $("threadsLabel").hidden = cpuSel.value !== ""; render(); });
  [ramSel, threadsSel, stSel].forEach(function (s) { s.addEventListener("change", render); });
})();
