#!/usr/bin/env python3
"""Genera /en/index.html, /es/index.html, /index.html y assets/strings.js desde src/template.html.
Uso: python3 build.py  [--base https://tudominio.com]
"""
import json, sys, pathlib

ROOT = pathlib.Path(__file__).parent
BASE = "https://example.com"
if "--base" in sys.argv:
    BASE = sys.argv[sys.argv.index("--base") + 1].rstrip("/")

# ---- Textos estáticos (se renderizan en el HTML para SEO) ----
S = {
 "meta_title": ("PortRace VI — The race to port GTA VI to PC + PC compatibility check",
                "PortRace VI — La carrera por portear GTA VI a PC + verificador de compatibilidad"),
 "meta_desc": ("Unofficial tracker of the community projects trying to run GTA VI on PC (Leonida, VIctory, XCL, Xbox2Windows) and a free check to see if your PC could handle it.",
               "Rastreador no oficial de los proyectos comunitarios que intentan correr GTA VI en PC (Leonida, VIctory, XCL, Xbox2Windows) y un verificador gratis para ver si tu PC lo aguantaría."),
 "nav_race": ("The race", "La carrera"), "nav_check": ("Can I run it?", "¿Lo corre mi PC?"), "nav_faq": ("FAQ", "FAQ"),
 "hero_kicker": ("Community tracker · Unofficial", "Rastreador comunitario · No oficial"),
 "hero_l1": ("The race to port", "La carrera por portear"),
 "hero_l2": ("GTA VI to PC", "GTA VI a PC"),
 "hero_sub": ("Rockstar hasn't announced a PC version. The community is racing anyway. Follow every project, honestly sourced, and find out if your rig could handle it.",
              "Rockstar no ha anunciado versión de PC. La comunidad corre igual. Sigue cada proyecto con fuentes honestas y descubre si tu PC lo aguantaría."),
 "cta_check": ("Check my PC", "Revisar mi PC"), "cta_race": ("See the race", "Ver la carrera"),
 "scam_title": ("Scam alert", "Alerta de estafa"),
 "scam_body": ("There is no official GTA VI PC download. Anything offering a \"GTA 6 PC port\" installer or launcher is fake or malware. Reported examples include a so-called \"Kerberus Launcher\".",
               "No existe descarga oficial de GTA VI para PC. Todo lo que ofrezca un instalador o launcher de \"GTA 6 PC\" es falso o malware. Se ha reportado, por ejemplo, un supuesto \"Kerberus Launcher\"."),
 "race_kicker": ("Live tracker", "Tracker en vivo"),
 "race_title": ("Who's closest?", "¿Quién va más cerca?"),
 "race_sub": ("Six milestones per project, weighted by difficulty. Every status needs evidence and we show where it comes from.",
              "Seis hitos por proyecto, ponderados por dificultad. Cada estado necesita evidencia y mostramos de dónde viene."),
 "lg_done": ("Done", "Hecho"), "lg_wip": ("In progress", "En progreso"), "lg_todo": ("Not yet", "Aún no"), "lg_unknown": ("Unknown", "Desconocido"),
 "check_kicker": ("Free tool", "Herramienta gratis"),
 "check_title": ("Can your PC run it?", "¿Tu PC lo corre?"),
 "check_sub": ("We auto-detect what the browser lets us see and you confirm the rest. Nothing leaves your device.",
               "Detectamos lo que el navegador nos deja ver y tú confirmas el resto. Nada sale de tu dispositivo."),
 "f_gpu": ("Graphics card", "Tarjeta gráfica"), "f_vram": ("VRAM", "VRAM"), "f_ram": ("System RAM", "RAM del sistema"),
 "f_cpu": ("CPU threads", "Hilos de CPU"), "f_storage": ("Storage", "Almacenamiento"),
 "check_disclaimer": ("There are no official PC requirements. This is an estimate that treats the Xbox Series X as the console-class baseline. A real port may need more or less.",
                      "No hay requisitos oficiales de PC. Es una estimación que toma la Xbox Series X como base de nivel consola. Un port real podría pedir más o menos."),
 "faq_title": ("Straight answers", "Respuestas directas"),
 "q1": ("Is there an official PC version?", "¿Existe versión oficial para PC?"),
 "a1": ("No. Rockstar has announced GTA VI for PS5 and Xbox Series X|S and has not given a PC date. Estimates for an eventual PC release are speculation. The past gaps were roughly 13 months for RDR2 and 19 months for GTA V.",
        "No. Rockstar anunció GTA VI para PS5 y Xbox Series X|S y no ha dado fecha para PC. Las estimaciones son especulación. Los precedentes fueron unos 13 meses en RDR2 y 19 meses en GTA V."),
 "q2": ("Can I play it with these projects today?", "¿Puedo jugarlo hoy con estos proyectos?"),
 "a2": ("No. None of them is playable. The most advanced reports reach menus and loading, but the world does not render properly, and at least one warns it can crash your graphics driver. Treat them as engineering research, not a way to play.",
        "No. Ninguno es jugable. Los reportes más avanzados llegan a menús y carga, pero el mundo no se renderiza bien, y al menos uno advierte que puede tumbar el driver gráfico. Tómalos como investigación de ingeniería, no como una forma de jugar."),
 "q3": ("Is this legal?", "¿Esto es legal?"),
 "a3": ("This site hosts and links no game files, builds or keys, and we never will. The projects say they ship no copyrighted data and need files you supply, but they target a build that reportedly leaked, and Take-Two has a history of takedowns against fan projects. We are a tracker and do not give legal advice. The safest option is to wait for an official release.",
        "Este sitio no aloja ni enlaza archivos del juego, builds ni claves, y nunca lo hará. Los proyectos dicen no incluir datos con copyright y requerir archivos que tú aportes, pero apuntan a un build que según los reportes se filtró, y Take-Two tiene historial de takedowns contra proyectos de fans. Somos un tracker y no damos asesoría legal. Lo más seguro es esperar una versión oficial."),
 "q4": ("How accurate is the PC check?", "¿Qué tan preciso es el verificador?"),
 "a4": ("It is a rough estimate. Browsers hide exact hardware, so you confirm RAM, CPU and storage yourself, and the GPU table uses approximate relative performance. It will improve once real PC performance data exists.",
        "Es una estimación aproximada. Los navegadores ocultan el hardware exacto, así que confirmas tú RAM, CPU y almacenamiento, y la tabla de GPUs usa rendimiento relativo aproximado. Mejorará cuando haya datos reales de rendimiento en PC."),
 "q5": ("Are you affiliated with Rockstar, Take-Two or these projects?", "¿Tienen relación con Rockstar, Take-Two o estos proyectos?"),
 "a5": ("No. PortRace VI is an independent fan-made tracker.", "No. PortRace VI es un tracker independiente hecho por fans."),
 "foot_disclaimer": ("PortRace VI is an unofficial fan project. Not affiliated with or endorsed by Rockstar Games, Take-Two Interactive, or any of the tracked projects. Grand Theft Auto and related names are trademarks of their respective owners. Visual style is inspired by the game's setting and uses no official assets.",
                     "PortRace VI es un proyecto de fans no oficial. No está afiliado ni respaldado por Rockstar Games, Take-Two Interactive ni por ninguno de los proyectos rastreados. Grand Theft Auto y los nombres relacionados son marcas de sus respectivos dueños. El estilo visual se inspira en la ambientación del juego y no usa assets oficiales."),
 "foot_correct": ("Spot something wrong? Corrections with a source are welcome.", "¿Ves algo incorrecto? Se agradecen correcciones con fuente."),
}

# ---- Textos dinámicos (los usa app.js) ----
J = {
 "projects": ("projects tracked", "proyectos rastreados"),
 "playable": ("playable builds", "builds jugables"),
 "official": ("official PC date", "fecha oficial PC"),
 "none": ("None", "Ninguna"),
 "of": ("of", "de"),
 "milestones": ("milestones", "hitos"),
 "repo": ("GitHub repo", "Repo en GitHub"),
 "repoPending": ("Repo link pending verification", "Enlace al repo pendiente de verificar"),
 "sources": ("Sources", "Fuentes"),
 "by": ("by", "por"),
 "updated": ("Last verified", "Última verificación"),
 "meta": ("", ""),
 "commits": ("Commits", "Commits"), "commitsWord": ("commits", "commits"), "lastCommit": ("Last commit", "Último commit"),
 "readmeChanged": ("README change detected", "Cambio de README detectado"), "watcher": ("Watcher last ran", "El vigilante corrió por última vez"),
 "unavailable": ("Repository unavailable. Possible takedown.", "Repositorio no disponible. Posible takedown."), "issues": ("Issues", "Issues"),
 "score": ("Progress score", "Puntaje de avance"), "evidence": ("Evidence", "Evidencia"), "checked": ("Checked", "Verificado"),
 "pushed": ("last push", "último push"), "agoNow": ("just now", "justo ahora"), "agoMin": ("%n min ago", "hace %n min"),
 "agoHour": ("%n h ago", "hace %n h"), "agoDay": ("%n d ago", "hace %n d"),
 "ekReadme": ("Project README", "README del proyecto"), "ekInferred": ("Our inference", "Inferencia nuestra"),
 "ekDiscord": ("Discord, relayed, unverified", "Discord, relayado, sin verificar"), "ekPress": ("Press", "Prensa"),
 "autodetected": ("Auto-detected: ", "Detectado automáticamente: "),
 "notDetected": ("Could not detect, please choose.", "No se pudo detectar, elige una opción."),
 "browserCap": ("Browsers report at most 8 GB, so please confirm.", "Los navegadores reportan máximo 8 GB, confírmalo."),
 "threadsDetected": ("Detected %n threads", "Detectados %n hilos"),
 "unknownGpu": ("Other / not listed", "Otra / no aparece"),
 "pickGpu": ("Choose your GPU…", "Elige tu GPU…"),
 "laptopNote": ("Laptop GPU detected: performance reduced ~25%.", "GPU de portátil detectada: rendimiento reducido ~25%."),
 "appleNote": ("Apple Silicon has no Windows/Vulkan path for these projects.", "Apple Silicon no tiene ruta Windows/Vulkan para estos proyectos."),
 "mobileNote": ("Open this page on your PC for an accurate check.", "Abre esta página en tu PC para un chequeo preciso."),
 "hdd": ("HDD (hard drive)", "HDD (disco duro)"), "sata": ("SATA SSD", "SSD SATA"), "nvme": ("NVMe SSD", "SSD NVMe"),
 "gb": ("GB", "GB"),
 "rowGpu": ("GPU power", "Potencia GPU"), "rowVram": ("VRAM", "VRAM"), "rowRam": ("RAM", "RAM"), "rowCpu": ("CPU", "CPU"), "rowStorage": ("Storage", "Almacenamiento"),
 "yourVerdict": ("Your verdict", "Tu veredicto"),
 "pickPrompt": ("Choose your GPU to see your result.", "Elige tu GPU para ver tu resultado."),
 "verdict": [
   ("Not today", "Hoy no"), ("Minimum", "Mínimo"), ("Console-class", "Nivel consola"), ("High-end", "Gama alta"), ("Ultra", "Ultra")],
 "verdictDesc": [
   ("Below Xbox Series S-class. It would struggle badly or not run.", "Por debajo de una Xbox Series S. Sufriría mucho o no correría."),
   ("About Xbox Series S-class: low settings, 30 fps at best.", "Cerca de una Xbox Series S: ajustes bajos, 30 fps como mucho."),
   ("About Xbox Series X-class: 30 fps, near console settings.", "Cerca de una Xbox Series X: 30 fps, ajustes similares a consola."),
   ("Comfortably above console: high settings, 60 fps possible.", "Claramente sobre consola: ajustes altos, 60 fps posibles."),
   ("Far above console: max settings, high resolution.", "Muy sobre consola: ajustes máximos, alta resolución.")],
 "bottleneck": ("Biggest limit: %c. Upgrade it to reach the next tier.", "Mayor limitante: %c. Mejóralo para subir de nivel."),
 "noBottleneck": ("Nothing is holding you back.", "Nada te está limitando."),
 "tag": [("No", "No"), ("Min", "Mín"), ("OK", "OK"), ("Great", "Muy bien"), ("Top", "Top")],
 "shareText": ("My PC rates \"%v\" for GTA VI on PC (estimate). Check yours:", "Mi PC sale \"%v\" para GTA VI en PC (estimado). Revisa la tuya:"),
 "copyBtn": ("Copy result", "Copiar resultado"), "copied": ("Copied!", "¡Copiado!"),
 "imgBtn": ("Download card", "Descargar tarjeta"), "shareBtn": ("Share", "Compartir"),
 "cardSub": ("GTA VI on PC · compatibility estimate", "GTA VI en PC · estimación de compatibilidad"),
}


# ======================================================================
#  SEO + páginas generadas
# ======================================================================
import re, datetime, html as _h

for k in ("scam_title", "scam_body"):
    S.pop(k, None)

S.update({
 "meta_title": ("GTA 6 PC: Can Your PC Run It? Requirements & Port Progress",
                "GTA 6 PC: ¿Lo corre tu PC? Requisitos y progreso del port"),
 "meta_desc": ("Unofficial tracker of the GTA VI PC port projects (Leonida, VIctory, XCL), estimated PC requirements and a free CPU and GPU check.",
               "Rastreador no oficial del port de GTA VI a PC (Leonida, VIctory, XCL), requisitos estimados y verificador gratis de CPU y GPU."),
 "nav_req": ("Requirements", "Requisitos"),
 "nav_when": ("PC date", "Fecha en PC"),
 "nav_leak": ("The leak", "La filtración"),
 "f_cpu": ("CPU (processor)", "CPU (procesador)"),
 "f_threads": ("CPU threads (only if you don't know the model)", "Hilos de CPU (solo si no sabes el modelo)"),
 "req_kicker": ("Estimated requirements", "Requisitos estimados"),
 "req_title": ("GTA 6 PC requirements (estimated)", "Requisitos de GTA 6 en PC (estimados)"),
 "req_sub": ("There are no official specs yet. These tiers use the Xbox Series X as the baseline and match the PC checker above.",
             "Aún no hay specs oficiales. Estos niveles usan la Xbox Series X como base y coinciden con el verificador de arriba."),
 "req_note": ("Estimates only. A real port could ask for more or less. GPU and CPU examples are approximate relative performance, not exact equivalents.",
              "Solo estimaciones. Un port real podría pedir más o menos. Los ejemplos de GPU y CPU son rendimiento relativo aproximado, no equivalencias exactas."),
 "gpu_index_link": ("See the GPU compatibility list", "Ver la lista de compatibilidad por GPU"),
})
J.update({
 "cpuUnknown": ("I don't know / not listed", "No sé / no aparece"),
 "cpuHintBrowser": ("Browsers can't read your CPU model. Find it in Task Manager → Performance → CPU.",
                    "Los navegadores no pueden leer tu modelo de CPU. Búscalo en Administrador de tareas → Rendimiento → CPU."),
 "threadsWord": ("threads", "hilos"),
})

TODAY = datetime.date.today().isoformat()
LANGS2 = ("en", "es")
LI = {"en": 0, "es": 1}
OGLOC = {"en": "en_US", "es": "es_ES"}

def esc(s): return _h.escape(s, quote=True)
def slugify(label):
    s = re.sub(r"\(.*?\)", "", label).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

GPUS = [dict(re=g[0], label=g[1], score=g[2], vram=g[3], slug=slugify(g[1]))
        for g in json.load(open(ROOT / "src/gpus.json", encoding="utf-8"))]
assert len({g["slug"] for g in GPUS}) == len(GPUS), "slugs duplicados"
CPUS = [dict(brand=c[0], label=c[1], threads=c[2], score=c[3])
        for c in json.load(open(ROOT / "src/cpus.json", encoding="utf-8"))]
(ROOT / "assets/gpus.js").write_text("window.GPUS_RAW=" + json.dumps(GPUS, ensure_ascii=False) + ";\n", encoding="utf-8")
(ROOT / "assets/cpus.js").write_text("window.CPUS_RAW=" + json.dumps(CPUS, ensure_ascii=False) + ";\n", encoding="utf-8")

# ---- espejo exacto de la lógica de app.js ----
def lvl(v, cuts): return sum(1 for c in cuts if v >= c)
RAMLV = {8: 0, 16: 2, 32: 3, 64: 4}
def gpu_lvl(g): return lvl(g["score"], [50, 95, 150, 250])
def vram_lvl(g): return lvl(g["vram"], [6, 10, 16, 24])
def overall(g, ram, cpu_score):  # almacenamiento NVMe
    return min(gpu_lvl(g), vram_lvl(g), RAMLV[ram], lvl(cpu_score, [70, 95, 150, 210]), 4)

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;700&display=swap">')
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E"
           "%3Cstop offset='0' stop-color='%23ff4f8b'/%3E%3Cstop offset='1' stop-color='%23ff9a5a'/%3E%3C/linearGradient%3E%3C/defs%3E%3Ccircle cx='16' cy='16' r='14' fill='url(%23g)'/%3E%3C/svg%3E")

FILEFIX = r'''<script>if(location.protocol==="file:")document.addEventListener("DOMContentLoaded",function(){document.querySelectorAll("a[href]").forEach(function(a){var h=a.getAttribute("href"),m=h.match(/^([^?#]*)(.*)$/);if(m[1]&&!/^[a-z]+:/i.test(m[1])&&/\/$/.test(m[1]))a.setAttribute("href",m[1]+"index.html"+m[2])})})</script>'''

def jsonld(objs):
    return '<script type="application/ld+json">' + json.dumps(objs, ensure_ascii=False).replace("</", "<\\/") + "</script>"

def seo_head(lang, title, desc, rest, og_type="website"):
    canon = f"{BASE}/{lang}/{rest}"
    L = [f"<title>{esc(title)}</title>",
         f'<meta name="description" content="{esc(desc)}">',
         f'<link rel="canonical" href="{canon}">',
         '<meta name="robots" content="index,follow,max-image-preview:large">',
         '<meta name="theme-color" content="#0a0a0f">',
         f'<link rel="icon" href="{FAVICON}">']
    for l in LANGS2:
        L.append(f'<link rel="alternate" hreflang="{l}" href="{BASE}/{l}/{rest}">')
    L.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}/en/{rest}">')
    other = "es" if lang == "en" else "en"
    L += [f'<meta property="og:title" content="{esc(title)}">',
          f'<meta property="og:description" content="{esc(desc)}">',
          f'<meta property="og:type" content="{og_type}">',
          f'<meta property="og:url" content="{canon}">',
          '<meta property="og:site_name" content="PortRace VI">',
          f'<meta property="og:locale" content="{OGLOC[lang]}">',
          f'<meta property="og:locale:alternate" content="{OGLOC[other]}">',
          f'<meta property="og:image" content="{BASE}/assets/og.png">',
          '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
          '<meta property="og:image:alt" content="PortRace VI: GTA VI on PC tracker and compatibility check">',
          '<meta name="twitter:card" content="summary_large_image">',
          f'<meta name="twitter:title" content="{esc(title)}">',
          f'<meta name="twitter:description" content="{esc(desc)}">',
          f'<meta name="twitter:image" content="{BASE}/assets/og.png">']
    return "\n".join(L)

# ---- tabla de requisitos (coincide con los umbrales del verificador) ----
REQH = (("Tier", "GPU", "VRAM", "RAM", "CPU", "Storage", "What to expect"),
        ("Nivel", "GPU", "VRAM", "RAM", "CPU", "Almacenamiento", "Qué esperar"))
REQR = [
 (1, ("≈ GTX 1060 / RX 580 or better (about Xbox Series S)", "≈ GTX 1060 / RX 580 o superior (similar a Xbox Series S)"), "6 GB+", "16 GB",
     ("≈ Ryzen 5 2600 / Core i5-9400F", "≈ Ryzen 5 2600 / Core i5-9400F"), ("SATA SSD", "SSD SATA"),
     ("Low settings, about 30 fps", "Ajustes bajos, unos 30 fps")),
 (2, ("≈ RX 5700 / RTX 3060 Ti / RX 6600 XT or better", "≈ RX 5700 / RTX 3060 Ti / RX 6600 XT o superior"), "10 GB+", "16 GB",
     ("≈ Ryzen 5 3600 / Core i5-11400F", "≈ Ryzen 5 3600 / Core i5-11400F"), ("SATA SSD", "SSD SATA"),
     ("Console settings, about 30 fps (Xbox Series X level)", "Ajustes de consola, unos 30 fps (nivel Xbox Series X)")),
 (3, ("≈ RX 6800 / RX 7800 XT / RTX 4070 Ti SUPER or better (16 GB VRAM)", "≈ RX 6800 / RX 7800 XT / RTX 4070 Ti SUPER o superior (16 GB de VRAM)"), "16 GB+", "32 GB",
     ("≈ Ryzen 7 5800X / Core i7-12700K", "≈ Ryzen 7 5800X / Core i7-12700K"), ("NVMe SSD", "SSD NVMe"),
     ("High settings, 60 fps possible", "Ajustes altos, 60 fps posibles")),
 (4, ("≈ RTX 4090 / RTX 5090 / RX 7900 XTX", "≈ RTX 4090 / RTX 5090 / RX 7900 XTX"), "24 GB+", "64 GB",
     ("≈ Ryzen 7 7800X3D / Core i9-13900K", "≈ Ryzen 7 7800X3D / Core i9-13900K"), ("NVMe SSD", "SSD NVMe"),
     ("Max settings, high resolution", "Ajustes máximos, alta resolución")),
]
def req_table(lang):
    i = LI[lang]
    head = "".join(f"<th>{esc(x)}</th>" for x in REQH[i])
    rows = ""
    for t, gpu, vram, ram, cpu, st, ex in REQR:
        rows += (f"<tr><th>{esc(J['verdict'][t][i])}</th><td>{esc(gpu[i])}</td><td>{vram}</td><td>{ram}</td>"
                 f"<td>{esc(cpu[i])}</td><td>{esc(st[i])}</td><td>{esc(ex[i])}</td></tr>")
    return f'<div class="tablewrap"><table class="req"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'

# ---- preguntas frecuentes → JSON-LD ----
def faq_ld(lang):
    i = LI[lang]
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": S[f"q{n}"][i],
         "acceptedAnswer": {"@type": "Answer", "text": S[f"a{n}"][i]}} for n in range(1, 6)]}

# ---- piezas comunes de las páginas generadas ----
def header_html(lang, depth, rest):
    i = LI[lang]; up = "../" * (depth - 1); root = "../" * depth
    other = "es" if lang == "en" else "en"
    cur = {l: ('aria-current="true"' if l == lang else "") for l in LANGS2}
    return (f'<header class="top"><div class="wrap"><a class="logo" href="{up or "./"}">PortRace <b>VI</b></a>'
            f'<nav class="main"><a href="{up}#race">{S["nav_race"][i]}</a><a href="{up}#check">{S["nav_check"][i]}</a>'
            f'<a href="{up}#when">{S["nav_when"][i]}</a><a href="{up}#leak">{S["nav_leak"][i]}</a><a href="{up}#req">{S["nav_req"][i]}</a><a href="{up}#faq">{S["nav_faq"][i]}</a></nav>'
            f'<div class="lang" role="group" aria-label="Language">'
            f'<a href="{root}en/{rest}" hreflang="en" {cur["en"]}>EN</a><a href="{root}es/{rest}" hreflang="es" {cur["es"]}>ES</a></div></div></header>')

def footer_html(lang, depth):
    i = LI[lang]; up = "../" * (depth - 1)
    return (f'<footer><div class="wrap"><div class="mega" aria-hidden="true">PortRace VI</div><p><a href="{up}">PortRace VI</a> · <a href="{up}gpu/">{esc(S["gpu_index_link"][i])}</a></p>'
            f'<p>{esc(S["foot_disclaimer"][i])}</p><p>{esc(S["foot_correct"][i])}</p></div></footer>')

def shell(lang, depth, rest, title, desc, body, ld):
    root = "../" * depth
    return (f'<!doctype html>\n<html lang="{lang}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">\n<script>document.documentElement.classList.add("js")</script>\n'
            f'{seo_head(lang, title, desc, rest)}\n{FONTS}\n<link rel="stylesheet" href="{root}assets/styles.css">\n{jsonld(ld)}\n</head><body>\n'
            f'{header_html(lang, depth, rest)}\n<main id="top">{body}</main>\n{footer_html(lang, depth)}\n<script src="{root}assets/fx.js"></script>\n{FILEFIX}\n</body></html>')

def crumbs(lang, depth, items):
    parts = " <span>/</span> ".join(f'<a href="{href}">{esc(t)}</a>' if href else f"<span>{esc(t)}</span>" for t, href in items)
    return f'<div class="crumbs">{parts}</div>'

def bc_ld(lang, items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": n + 1, "name": t, "item": u} for n, (t, u) in enumerate(items)]}

def hero(inner):
    return f'<div class="pagehero"><div class="orb o1"></div><div class="orb o2"></div><div class="wrap">{inner}</div></div>'

# ---- páginas por GPU ----
SHORT = {
 "en": ["Probably not: its estimated power is below an Xbox Series S.",
        "Barely: expect minimum-class performance, low settings and about 30 fps at best.",
        "Likely yes, at console-class settings (around Xbox Series X level).",
        "Yes, with room above console: high settings, 60 fps possible.",
        "Easily: it sits at the top end of what a PC port could ask for."],
 "es": ["Probablemente no: su potencia estimada está por debajo de una Xbox Series S.",
        "Justo: espera rendimiento de nivel mínimo, ajustes bajos y unos 30 fps como mucho.",
        "Probablemente sí, con ajustes de nivel consola (cerca de una Xbox Series X).",
        "Sí, con margen sobre consola: ajustes altos y 60 fps posibles.",
        "De sobra: está en lo más alto de lo que podría pedir un port de PC."],
}
def gpu_page(lang, g, ranked):
    i = LI[lang]; name = g["label"]; v = J["verdict"]
    gl, vl = gpu_lvl(g), vram_lvl(g); t = min(gl, vl)
    mid, high = overall(g, 16, 95), overall(g, 32, 150)
    short = SHORT[lang][t]
    pct = round(g["score"])
    if lang == "en":
        title = f"Can the {name} run GTA 6 on PC? Estimate | PortRace VI"
        desc = f"Can the {name} run GTA VI on PC? {short} "
        h1 = f"Can the {name} run GTA 6 on PC?"
        lead = f"{short} There is no official PC version yet, so this is an estimate that treats Xbox Series X-class performance as the baseline."
        limit = (f"The limit is VRAM: {g['vram']} GB is below what a console-class experience would likely want (about 10 GB or more), even though the GPU's raw power is higher." if vl < gl else
                 "The limit is raw GPU power rather than memory." if gl < vl else
                 "GPU power and VRAM are balanced for this tier.")
        how = ("We compare each GPU against an Xbox Series X baseline of 100 points. Minimum starts at 50 points, console-class at 95, high-end at 150 and ultra at 250. VRAM, RAM, CPU and storage also count, and the weakest part sets your tier. Laptop versions of a GPU can perform around 25% lower.")
        labels = ("Estimated power", "VRAM", "GPU-only tier", "Typical mid-range PC (16 GB RAM, Ryzen 5 3600-class)", "Typical high-end PC (32 GB RAM, Ryzen 7 5800X-class)")
        power = f"{pct} pts (≈ {pct}% of an Xbox Series X)"
        h_num, h_limit, h_how, h_sim = "The numbers", "What limits it", "How we estimate", "Similar GPUs"
        cta = "Check my full PC with this GPU"
        crumb = ("Home", "GPU list", name)
        faqq = f"Can the {name} run GTA 6 on PC?"
        faqa = f"{short} There is no official PC version yet; this is an estimate."
    else:
        title = f"¿La {name} corre GTA 6 en PC? Estimación | PortRace VI"
        desc = f"¿La {name} corre GTA VI en PC? {short} "
        h1 = f"¿La {name} corre GTA 6 en PC?"
        lead = f"{short} Todavía no hay versión oficial para PC, así que es una estimación que toma el rendimiento de una Xbox Series X como base."
        limit = (f"El límite es la VRAM: {g['vram']} GB queda por debajo de lo que probablemente pediría una experiencia de nivel consola (unos 10 GB o más), aunque la potencia bruta de la GPU sea mayor." if vl < gl else
                 "El límite es la potencia bruta de la GPU, no la memoria." if gl < vl else
                 "La potencia de la GPU y la VRAM están equilibradas para este nivel.")
        how = ("Comparamos cada GPU con una base de Xbox Series X de 100 puntos. El mínimo empieza en 50 puntos, el nivel consola en 95, la gama alta en 150 y el ultra en 250. También cuentan VRAM, RAM, CPU y almacenamiento, y la pieza más débil fija tu nivel. Las versiones para portátil de una GPU pueden rendir un 25% menos.")
        labels = ("Potencia estimada", "VRAM", "Nivel solo por GPU", "PC de gama media típico (16 GB de RAM, nivel Ryzen 5 3600)", "PC de gama alta típico (32 GB de RAM, nivel Ryzen 7 5800X)")
        power = f"{pct} pts (≈ {pct}% de una Xbox Series X)"
        h_num, h_limit, h_how, h_sim = "Los números", "Qué la limita", "Cómo lo estimamos", "GPUs similares"
        cta = "Revisar mi PC completo con esta GPU"
        crumb = ("Inicio", "Lista de GPUs", name)
        faqq = f"¿La {name} corre GTA 6 en PC?"
        faqa = f"{short} Todavía no hay versión oficial para PC; es una estimación."
    rows = [(labels[0], power, None), (labels[1], f"{g['vram']} GB", None), (labels[2], v[t][i], t),
            (labels[3], v[mid][i], mid), (labels[4], v[high][i], high)]
    rows_html = "".join(
        f'<div class="row"><div><b>{esc(a)}</b>{esc(b)}</div>' + (f'<span class="tag t{c}">{esc(J["tag"][c][i])}</span>' if c is not None else "") + "</div>"
        for a, b, c in rows)
    near = sorted((x for x in ranked if x is not g), key=lambda x: abs(x["score"] - g["score"]))[:6]
    sim = "".join(f'<li><a href="../{x["slug"]}/">{esc(x["label"])}<small>{esc(v[min(gpu_lvl(x), vram_lvl(x))][i])}</small></a></li>' for x in near)
    body = (hero(crumbs(lang, 3, [(crumb[0], "../../"), (crumb[1], "../"), (crumb[2], None)]) + f"<h1>{esc(h1)}</h1><p>{esc(lead)}</p>")
            + '<section><div class="wrap"><div class="gpu-grid"><div>'
            f'<div class="res-top"><span class="label">{esc(J["yourVerdict"][i])}</span><h3>{esc(v[t][i])}</h3><p>{esc(J["verdictDesc"][t][i])}</p></div>'
            f'<h2 class="brandh">{esc(h_num)}</h2><div class="rows">{rows_html}</div>'
            f'<p style="margin-top:22px"><a class="btn pri" href="../../?gpu={g["slug"]}#check">{esc(cta)}</a></p></div>'
            f'<div class="prose"><h2>{esc(h_limit)}</h2><p>{esc(limit)}</p><h2>{esc(h_how)}</h2><p>{esc(how)}</p></div></div></div></section>'
            f'<section class="alt"><div class="wrap"><div class="head"><h2>{esc(h_sim)}</h2></div><ul class="linklist">{sim}</ul></div></section>')
    rest = f"gpu/{g['slug']}/"
    ld = {"@context": "https://schema.org", "@graph": [
        bc_ld(lang, [(crumb[0], f"{BASE}/{lang}/"), (crumb[1], f"{BASE}/{lang}/gpu/"), (crumb[2], f"{BASE}/{lang}/{rest}")]),
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": faqq, "acceptedAnswer": {"@type": "Answer", "text": faqa}}]}]}
    return shell(lang, 3, rest, title, desc, body, ld)

def gpu_index(lang, ranked):
    i = LI[lang]; v = J["verdict"]
    if lang == "en":
        title = "GTA 6 PC GPU Compatibility List (RTX, Radeon, Arc) | PortRace VI"
        desc = "Estimated GTA VI PC compatibility for every popular NVIDIA GeForce, AMD Radeon and Intel Arc GPU. Find yours and see your tier."
        h1, lead = "Can your GPU run GTA 6 on PC?", "Pick your graphics card to see an estimated tier. There is no official PC version yet, so these are estimates."
        crumb = ("Home", "GPU list")
    else:
        title = "Lista de compatibilidad GPU para GTA 6 PC (RTX, Radeon, Arc) | PortRace VI"
        desc = "Compatibilidad estimada de GTA VI en PC para las GPU populares de NVIDIA GeForce, AMD Radeon e Intel Arc. Busca la tuya y mira tu nivel."
        h1, lead = "¿Tu GPU corre GTA 6 en PC?", "Elige tu tarjeta gráfica para ver un nivel estimado. Todavía no hay versión oficial para PC, así que son estimaciones."
        crumb = ("Inicio", "Lista de GPUs")
    groups = [("NVIDIA", [g for g in ranked if g["label"].startswith("GeForce")]),
              ("AMD", [g for g in ranked if g["label"].startswith("Radeon")]),
              ("Intel", [g for g in ranked if g["label"].startswith("Intel")])]
    secs = ""
    for name, items in groups:
        li = "".join(f'<li><a href="{g["slug"]}/">{esc(g["label"])}<small>{esc(v[min(gpu_lvl(g), vram_lvl(g))][i])}</small></a></li>' for g in items)
        secs += f'<h2 class="brandh">{name}</h2><ul class="linklist">{li}</ul>'
    body = hero(crumbs(lang, 2, [(crumb[0], "../"), (crumb[1], None)]) + f"<h1>{esc(h1)}</h1><p>{esc(lead)}</p>") + f'<section><div class="wrap">{secs}</div></section>'
    ld = {"@context": "https://schema.org", "@graph": [bc_ld(lang, [(crumb[0], f"{BASE}/{lang}/"), (crumb[1], f"{BASE}/{lang}/gpu/")])]}
    return shell(lang, 2, "gpu/", title, desc, body, ld)

# ======================================================================
#  Datos del tracker (fuente de verdad: src/data.json) + secciones nuevas
# ======================================================================
DATA = json.load(open(ROOT / "src/data.json", encoding="utf-8"))
_snap = ROOT / "src/snapshot.json"          # lo genera tools/watch.py (no se versiona)
if _snap.exists():
    _s = json.load(open(_snap, encoding="utf-8")); DATA["snapshot"] = _s["repos"]; DATA["snapshotAt"] = _s["fetched_at"]
(ROOT / "assets/data.js").write_text("window.RACE=" + json.dumps(DATA, ensure_ascii=False) + ";\n", encoding="utf-8")

MONTHS = {"en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
          "es": ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]}
KIND = {"confirmed": ("Confirmed by several outlets", "Confirmado por varios medios"), "reported": ("Reported", "Reportado"),
        "claimed": ("Claimed, unverified", "Afirmado, sin verificar"), "estimate": ("Third-party estimate", "Estimación de terceros"),
        "statement": ("Company statement", "Declaración de la empresa")}
CST = {"pending": ("Pending", "Pendiente"), "unproven": ("Unproven", "Sin probar"),
       "unconfirmed": ("Unconfirmed", "Sin confirmar"), "true": ("Reported true", "Reportado como cierto")}

def fmt_date(d, lang):
    parts = d.split("-")
    if len(parts) == 3: return f"{int(parts[2])} {MONTHS[lang][int(parts[1]) - 1]} {parts[0]}"
    if len(parts) == 2: return f"{MONTHS[lang][int(parts[1]) - 1]} {parts[0]}"
    return d
def mi(ym):  # índice de mes: 0 = nov 2026
    y, m = map(int, ym.split("-")); return (y - 2026) * 12 + (m - 11)
AXIS_N = 26  # nov 2026 .. dic 2028
def add_months(ymd, n):
    y, m, _ = map(int, ymd.split("-")); t = (y * 12 + m - 1) + n
    return f"{t // 12}-{t % 12 + 1:02d}"

# coherencia: la ventana oficial sale de lanzamiento + brechas históricas
_o = DATA["estimate"]["official"]
_ms = sorted(p["months"] for p in _o["precedents"])
assert add_months(_o["consoleLaunch"], _ms[0]) == _o["window"]["start"], "ventana oficial incoherente (inicio)"
assert add_months(_o["consoleLaunch"], _ms[-1]) == _o["window"]["end"], "ventana oficial incoherente (fin)"

def src_links(srcs):
    return '<div class="srcs">' + "".join(f'<a href="{esc(s["url"])}" rel="noopener nofollow" target="_blank">{esc(s["label"])} ↗</a>' for s in srcs) + "</div>"

def leak_section(lang):
    i = LI[lang]
    if lang == "en":
        kick, title = "Leak tracker", "The Cyberleek leak, day by day"
        sub = "What happened and what has been claimed, with press sources. We report this as news. We do not link to the leakers, their channels or any download, and we do not promote their token."
        h_claims, c_sub = "Claimed vs. reality", "Claims attributed to the group, checked against what is publicly known today. Statuses change as the projects move."
        due, cl_l, rl_l = "Verdict due", "Claim", "Reality"
    else:
        kick, title = "Tracker de la filtración", "La filtración de Cyberleek, día a día"
        sub = "Qué pasó y qué se ha afirmado, con fuentes de prensa. Lo contamos como noticia. No enlazamos a los filtradores, sus canales ni ninguna descarga, y no promovemos su token."
        h_claims, c_sub = "Prometido vs. real", "Afirmaciones atribuidas al grupo, contrastadas con lo que se sabe públicamente hoy. Los estados cambian a medida que avanzan los proyectos."
        due, cl_l, rl_l = "Veredicto", "Afirmación", "Realidad"
    tl = ""
    for e in DATA["events"]:
        tl += (f'<li><div class="tl-top"><span class="tl-date">{esc(fmt_date(e["date"], lang))}</span>'
               f'<span class="kind k-{e["kind"]}">{esc(KIND[e["kind"]][i])}</span></div>'
               f'<p>{esc(e["title"][lang])}</p>{src_links(e["sources"])}</li>')
    cl = ""
    for c in DATA["claims"]:
        chk = f' · {due}: {esc(fmt_date(c["check"], lang))}' if c.get("check") else ""
        cl += (f'<article class="claim"><div class="c-top"><h3>“{esc(c["claim"][lang])}”</h3>'
               f'<span class="st st-{c["status"]}">{esc(CST[c["status"]][i])}</span></div>'
               f'<p class="real"><b>{rl_l}:</b> {esc(c["reality"][lang])}{chk}</p>{src_links(c["sources"])}</article>')
    return (f'<section id="leak"><div class="wrap"><div class="head"><span class="label">{kick}</span><h2>{title}</h2><p>{esc(sub)}</p></div>'
            f'<ol class="timeline">{tl}</ol><h3 class="sub-h">{h_claims}</h3><p class="g-note">{esc(c_sub)}</p><div class="claims">{cl}</div></div></section>')

def fmt_int(n, lang): return f"{n:,}".replace(",", "." if lang == "es" else ",")

def eta_model():
    M = DATA["estimate"]["model"]; W = DATA["weights"]; order = [m["id"] for m in DATA["milestones"]]
    upto = order[:order.index(M["target"]) + 1]; today = datetime.date.fromisoformat(TODAY)
    rows = []
    for p in DATA["projects"]:
        st = p["status"]
        sc = sum(W[k] * (1 if st.get(k) == "done" else .5 if st.get(k) == "wip" else 0) for k in W)
        rem = sum(W[k] * (0 if st.get(k) == "done" else .5 if st.get(k) == "wip" else 1) for k in upto)
        age_real = (today - datetime.date.fromisoformat(p["started"])).days
        pace = sc / max(age_real, M["minAgeDays"]) if sc > 0 else 0
        days = {k: (round(rem / (pace * f)) if pace > 0 and rem > 0 else None) for k, f in M["decay"].items()}
        rows.append(dict(name=p["name"], score=sc, age=age_real, pace=pace, rem=rem, days=days))
    best = min((r for r in rows if r["days"]["realistic"]), key=lambda r: r["days"]["realistic"])
    o = DATA["estimate"]["official"]; launch = datetime.date.fromisoformat(o["consoleLaunch"])
    def addm(d, n): t = d.year * 12 + d.month - 1 + n; return datetime.date(t // 12, t % 12 + 1, min(d.day, 28))
    ms = sorted(x["months"] for x in o["precedents"]); o1, o2 = addm(launch, ms[0]), addm(launch, ms[-1])
    d1, d2 = (o1 - today).days, (o2 - today).days
    return dict(rows=rows, best=best, today=today, o1=o1, o2=o2, od=(d1, d2, (d1 + d2) // 2))

def dstr(d): return d.isoformat()
def plus(today, n): return today + datetime.timedelta(days=n)

def eta_block(lang):
    m = eta_model(); b = m["best"]; dd = b["days"]; t = m["today"]; od = m["od"]
    N = lambda n: fmt_int(n, lang)
    if lang == "en":
        l1, l2, u = "First playable community build (estimate)", "Official PC release (estimate)", "days"
        r1 = f"Range {N(dd['fast'])}–{N(dd['slow'])} days · around {fmt_date(dstr(plus(t, dd['realistic'])), lang)}"
        n1 = f"Based on the pace of {b['name']} and the other repos"
        r2 = f"Range {N(od[0])}–{N(od[1])} days · {fmt_date(dstr(m['o1'])[:7], lang)} – {fmt_date(dstr(m['o2'])[:7], lang)}"
        n2 = "Rockstar has not announced a PC version"
        foot = f"Editorial estimate computed on {fmt_date(TODAY, lang)}. It recalculates with every update and slides later if projects stall. Not a promise."
        how = "How it is calculated"
    else:
        l1, l2, u = "Primer build jugable de la comunidad (estimado)", "Lanzamiento oficial en PC (estimado)", "días"
        r1 = f"Rango {N(dd['fast'])}–{N(dd['slow'])} días · cerca del {fmt_date(dstr(plus(t, dd['realistic'])), lang)}"
        n1 = f"Según el ritmo de {b['name']} y de los otros repos"
        r2 = f"Rango {N(od[0])}–{N(od[1])} días · {fmt_date(dstr(m['o1'])[:7], lang)} – {fmt_date(dstr(m['o2'])[:7], lang)}"
        n2 = "Rockstar no ha anunciado versión de PC"
        foot = f"Estimación editorial calculada el {fmt_date(TODAY, lang)}. Se recalcula con cada actualización y se corre más adelante si los proyectos se frenan. No es una promesa."
        how = "Cómo se calcula"
    card = lambda cls, lab, n, rng, note: (f'<a class="eta-card {cls}" href="#when"><span class="eta-k">{esc(lab)}</span>'
        f'<span class="eta-n"><b data-count="{n}">{N(n)}</b><i>{u}</i></span><span class="eta-r">{esc(rng)}</span><span class="eta-t">{esc(note)}</span></a>')
    return (f'<div class="eta">{card("main", l1, dd["realistic"], r1, n1)}{card("alt", l2, od[2], r2, n2)}</div>'
            f'<p class="eta-foot">{esc(foot)} <a href="#when">{how} →</a></p>')

def when_block(lang, full):
    E = DATA["estimate"]; m = eta_model(); b = m["best"]; dd = b["days"]; t = m["today"]; od = m["od"]; o = E["official"]
    N = lambda n: fmt_int(n, lang)
    u = "days" if lang == "en" else "días"
    if lang == "en":
        lab = {"fast": "Community build, fast pace", "real": "Community build, realistic", "slow": "Community build, slow pace",
               "off": "Official Rockstar release on PC", "rum": "Rumor, unconfirmed: early 2027"}
        sub_off = f"{fmt_date(dstr(m['o1'])[:7], lang)} – {fmt_date(dstr(m['o2'])[:7], lang)} · about {N(od[2])} days"
        note = "Editorial estimate based on the pace of the repos. Not a promise."
        pros, cons = "Why it could be soon", "Why it could be late or never"
        th = ("Project", "Score", "Age (days)", "Pace (pts/day)", "Left to playable", "Fast", "Realistic", "Slow")
        hm = "How the days are calculated"
        how = ("Each project's progress score (0–10) divided by its age gives its pace in points per day. A repo younger than 3 days counts as 3, because repos are often published after private work. "
               "The work left until the Playable milestone is divided by that pace times a slowdown of 25% (fast), 5% (realistic) or 1% (slow), because what remains is harder than what is done. "
               "The headline uses the project with the shortest realistic time. If nothing changes, the age grows, the pace drops and the estimate slides later. "
               "The official window is the console launch (19 Nov 2026) plus the gaps seen on past Rockstar games (RDR2 +13 months, GTA V +19 months).")
        about = "about"
    else:
        lab = {"fast": "Build comunitario, ritmo rápido", "real": "Build comunitario, realista", "slow": "Build comunitario, ritmo lento",
               "off": "Lanzamiento oficial de Rockstar en PC", "rum": "Rumor, sin confirmar: inicios de 2027"}
        sub_off = f"{fmt_date(dstr(m['o1'])[:7], lang)} – {fmt_date(dstr(m['o2'])[:7], lang)} · unos {N(od[2])} días"
        note = "Estimación editorial basada en el ritmo de los repos. No es una promesa."
        pros, cons = "Por qué podría ser pronto", "Por qué podría ser tarde o nunca"
        th = ("Proyecto", "Puntaje", "Edad (días)", "Ritmo (pts/día)", "Falta para jugable", "Rápido", "Realista", "Lento")
        hm = "Cómo se calculan los días"
        how = ("El puntaje de avance de cada proyecto (0–10) dividido por su edad da su ritmo en puntos por día. Un repo de menos de 3 días cuenta como 3, porque los repos suelen publicarse tras trabajo privado. "
               "El trabajo que falta hasta el hito Jugable se divide por ese ritmo multiplicado por una desaceleración de 25% (rápido), 5% (realista) o 1% (lento), porque lo que queda es más difícil que lo hecho. "
               "El titular usa el proyecto con el menor tiempo realista. Si nada cambia, la edad crece, el ritmo baja y la estimación se corre más adelante. "
               "La ventana oficial es el lanzamiento en consola (19 nov 2026) más las brechas vistas en juegos anteriores de Rockstar (RDR2 +13 meses, GTA V +19 meses).")
        about = "cerca del"
    def drow(label, sub, num, cls=""):
        return (f'<li class="d-row {cls}"><div class="d-l"><b>{esc(label)}</b><span>{esc(sub)}</span></div>'
                f'<div class="d-n"><b>{num}</b><i>{u}</i></div></li>')
    comm = lambda key, k, cls="": drow(lab[key], f"{about} {fmt_date(dstr(plus(t, dd[k])), lang)}", N(dd[k]), cls)
    rows = comm("fast", "fast") + comm("real", "realistic", "hot") + comm("slow", "slow")
    rows += drow(lab["off"], sub_off, f"{N(od[0])}–{N(od[1])}")
    if full:
        ry, rm = map(int, o["rumor"]["start"].split("-")); ey, em = map(int, o["rumor"]["end"].split("-"))
        r0 = datetime.date(ry, rm, 1); r1 = datetime.date(ey + (em == 12), em % 12 + 1, 1) - datetime.timedelta(days=1)
        rows += drow(lab["rum"], f"{fmt_date(dstr(r0)[:7], lang)} – {fmt_date(dstr(r1)[:7], lang)}", f"{N((r0 - t).days)}–{N((r1 - t).days)}", "muted")
    out = f'<ul class="days">{rows}</ul><p class="edit-note">{esc(note)}</p>'
    if full:
        cell = lambda v: N(v) if v is not None else "—"
        trs = "".join(f"<tr><th>{esc(r['name'])}</th><td>{r['score']:.2f}</td><td>{r['age']}</td><td>{r['pace']:.2f}</td><td>{r['rem']:.2f}</td>"
                      f"<td>{cell(r['days']['fast'])}</td><td><b>{cell(r['days']['realistic'])}</b></td><td>{cell(r['days']['slow'])}</td></tr>"
                      for r in sorted(m["rows"], key=lambda r: (r["days"]["realistic"] is None, r["days"]["realistic"] or 0)))
        out += (f'<h3 class="sub-h">{esc(hm)}</h3><div class="tablewrap"><table class="req"><thead><tr>' + "".join(f"<th>{esc(x)}</th>" for x in th) +
                f'</tr></thead><tbody>{trs}</tbody></table></div><p class="edit-note">{esc(how)}</p>')
        out += (f'<div class="two"><div class="box"><h3>{pros}</h3><ul>' + "".join(f"<li>{esc(x[lang])}</li>" for x in E["pros"]) +
                f'</ul></div><div class="box"><h3>{cons}</h3><ul>' + "".join(f"<li>{esc(x[lang])}</li>" for x in E["cons"]) + "</ul></div></div>")
    return out

def when_section(lang):
    if lang == "en":
        kick, title, more = "PC release estimate, in days", "When could GTA 6 come to PC?", "See how it is calculated"
    else:
        kick, title, more = "Estimación de fecha en PC, en días", "¿Cuándo podría salir GTA 6 en PC?", "Ver cómo se calcula"
    return (f'<section id="when"><div class="wrap"><div class="head"><span class="label">{kick}</span><h2>{title}</h2></div>'
            f'{when_block(lang, False)}<p class="fine"><a href="gta-6-pc-release-date/">{more} →</a></p></div></section>')

RD_FAQ = {
 "en": [("When will GTA 6 come out on PC?",
         "Rockstar has not announced a PC version or a date. Based on the gaps between console and PC for Red Dead Redemption 2 (about 13 months) and GTA V (about 19 months), an official release would land between December 2027 and June 2028. This is an estimate, not an announcement."),
        ("Is there a rumored PC date?",
         "An early-2027 PC launch has been rumored and attributed to GamesBeat. Neither Rockstar nor Take-Two has confirmed it."),
        ("Can I play GTA 6 on PC today through community projects?",
         "No. None of the projects tracked here is playable. The furthest one reports reaching the game world with a black screen."),
        ("Who is Cyberleek?",
         "A group that claims to have leaked an Xbox build of GTA VI. We report the story with press sources in our leak tracker, but we do not link to the group or to any download.")],
 "es": [("¿Cuándo sale GTA 6 en PC?",
         "Rockstar no ha anunciado versión de PC ni fecha. Según las brechas entre consola y PC de Red Dead Redemption 2 (unos 13 meses) y GTA V (unos 19 meses), un lanzamiento oficial caería entre diciembre de 2027 y junio de 2028. Es una estimación, no un anuncio."),
        ("¿Hay una fecha rumoreada para PC?",
         "Se ha rumoreado un lanzamiento en PC a inicios de 2027, atribuido a GamesBeat. Ni Rockstar ni Take-Two lo han confirmado."),
        ("¿Puedo jugar GTA 6 en PC hoy con los proyectos de la comunidad?",
         "No. Ninguno de los proyectos rastreados aquí es jugable. El más avanzado reporta llegar al mundo del juego con pantalla negra."),
        ("¿Quién es Cyberleek?",
         "Un grupo que afirma haber filtrado un build de Xbox de GTA VI. Contamos la historia con fuentes de prensa en nuestro tracker de la filtración, pero no enlazamos al grupo ni a ninguna descarga.")],
}
def release_page(lang):
    i = LI[lang]
    if lang == "en":
        title = "When Will GTA 6 Come to PC? Estimated Date & Leaks | PortRace VI"
        desc = "Estimated GTA 6 PC release window from past Rockstar gaps and the leaked-build projects. See the timeline and what each source says."
        h1 = "When will GTA 6 come to PC?"; lead = "An estimated window for an official release and for an unofficial community build, with the reasoning behind each."
        crumb = ("Home", "When GTA 6 comes to PC"); faq_h = "Quick answers"; leak_link = "See the leak tracker"
    else:
        title = "¿Cuándo sale GTA 6 en PC? Fecha estimada y filtraciones | PortRace VI"
        desc = "Ventana estimada de GTA 6 en PC según las brechas de Rockstar y los proyectos del build filtrado. Mira la línea de tiempo y qué dice cada fuente."
        h1 = "¿Cuándo sale GTA 6 en PC?"; lead = "Una ventana estimada para un lanzamiento oficial y para un build comunitario no oficial, con el razonamiento de cada una."
        crumb = ("Inicio", "Cuándo sale GTA 6 en PC"); faq_h = "Respuestas rápidas"; leak_link = "Ver el tracker de la filtración"
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in RD_FAQ[lang])
    body = (hero(crumbs(lang, 2, [(crumb[0], "../"), (crumb[1], None)]) + f"<h1>{esc(h1)}</h1><p>{esc(lead)}</p>")
            + f'<section><div class="wrap">{when_block(lang, True)}<p class="fine"><a href="../#leak">{leak_link} →</a></p></div></section>'
            + f'<section class="alt"><div class="wrap"><div class="head"><h2>{faq_h}</h2></div>{faq}</div></section>')
    ld = {"@context": "https://schema.org", "@graph": [
        bc_ld(lang, [(crumb[0], f"{BASE}/{lang}/"), (crumb[1], f"{BASE}/{lang}/gta-6-pc-release-date/")]),
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in RD_FAQ[lang]]}]}
    return shell(lang, 2, "gta-6-pc-release-date/", title, desc, body, ld)


def marquee(lang):
    n = len(DATA["projects"])
    playable = sum(1 for p in DATA["projects"] if p["status"].get("play") == "done" and p["status"].get("stable") == "done")
    up = fmt_date(DATA["updated"], lang)
    dd = eta_model()["best"]["days"]["realistic"]
    items = (["GTA VI on PC", f"{n} projects racing", f"~{dd} days to a playable build (est.)", f"{playable} playable builds", "No official PC date", f"Updated {up}"] if lang == "en" else
             ["GTA VI en PC", f"{n} proyectos en carrera", f"~{dd} días para un build jugable (est.)", f"{playable} builds jugables", "Sin fecha oficial de PC", f"Actualizado {up}"])
    one = "".join(f'<span class="{"o" if k % 2 else ""}">{esc(t)}</span><i></i>' for k, t in enumerate(items))
    return f'<div class="marquee" aria-hidden="true"><div class="m-track">{one}{one}</div></div>'


# ======================================================================
#  Generación
# ======================================================================
ranked = sorted(GPUS, key=lambda g: -g["score"])
tpl = (ROOT / "src/template.html").read_text(encoding="utf-8")
urls = []   # rutas (sin idioma) para el sitemap

for lang in LANGS2:
    i = LI[lang]
    html = tpl.replace("{{lang}}", lang)
    html = html.replace("{{cur_en}}", 'aria-current="true"' if lang == "en" else "").replace("{{cur_es}}", 'aria-current="true"' if lang == "es" else "")
    for k, val in S.items():
        html = html.replace("{{%s}}" % k, val[i].replace("&", "&amp;"))
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "name": "PortRace VI", "url": f"{BASE}/{lang}/", "inLanguage": lang, "description": S["meta_desc"][i]},
        {"@type": "WebApplication", "name": ("GTA VI PC compatibility check" if lang == "en" else "Verificador de compatibilidad de GTA VI en PC"),
         "url": f"{BASE}/{lang}/#check", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
         "inLanguage": lang, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        faq_ld(lang)]}
    html = (html.replace("{{seo_head}}", seo_head(lang, S["meta_title"][i], S["meta_desc"][i], ""))
                .replace("{{fonts}}", FONTS).replace("{{jsonld}}", jsonld(ld)).replace("{{req_table}}", req_table(lang))
                .replace("{{eta_block}}", eta_block(lang)).replace("{{marquee}}", marquee(lang)).replace("{{when_section}}", when_section(lang)).replace("{{leak_section}}", leak_section(lang)))
    assert "{{" not in html, "placeholder sin resolver en " + lang
    (ROOT / lang).mkdir(exist_ok=True)
    (ROOT / lang / "index.html").write_text(html, encoding="utf-8")
    (ROOT / lang / "gta-6-pc-release-date").mkdir(exist_ok=True)
    (ROOT / lang / "gta-6-pc-release-date" / "index.html").write_text(release_page(lang), encoding="utf-8")
    (ROOT / lang / "gpu").mkdir(exist_ok=True)
    (ROOT / lang / "gpu" / "index.html").write_text(gpu_index(lang, ranked), encoding="utf-8")
    for g in GPUS:
        d = ROOT / lang / "gpu" / g["slug"]; d.mkdir(exist_ok=True)
        (d / "index.html").write_text(gpu_page(lang, g, ranked), encoding="utf-8")

urls = ["", "gta-6-pc-release-date/"] + ["gpu/"] + [f"gpu/{g['slug']}/" for g in GPUS]

# strings.js
def flat(i):
    out = {}
    for k, val in J.items():
        out[k] = [x[i] for x in val] if isinstance(val, list) else val[i]
    return out
(ROOT / "assets/strings.js").write_text("window.STR=" + json.dumps({l: flat(LI[l]) for l in LANGS2}, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")

# sitemap.xml con hreflang
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for u in urls:
    for l in LANGS2:
        sm.append(f"<url><loc>{BASE}/{l}/{u}</loc><lastmod>{TODAY}</lastmod>"
                  + "".join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{BASE}/{x}/{u}"/>' for x in LANGS2)
                  + f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/en/{u}"/></url>')
sm.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
(ROOT / ".nojekyll").write_text("", encoding="utf-8")

# raíz: redirige según idioma (con canonical y hreflang para buscadores)
(ROOT / "index.html").write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>PortRace VI</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="canonical" href="{BASE}/en/">
<link rel="alternate" hreflang="en" href="{BASE}/en/"><link rel="alternate" hreflang="es" href="{BASE}/es/"><link rel="alternate" hreflang="x-default" href="{BASE}/en/">
<script>var l=null;try{{var s=localStorage.getItem('lang');if(s==='es'||s==='en')l=s}}catch(e){{}}if(!l){{var L=navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||'en'];for(var i=0;i<L.length;i++){{var c=String(L[i]).slice(0,2).toLowerCase();if(c==='es'||c==='en'){{l=c;break}}}}}}location.replace((l||'en')+'/'+location.search+location.hash);</script>
<noscript><meta http-equiv="refresh" content="0;url=en/"></noscript></head>
<body style="background:#0a0a0f;color:#f4f4f7;font-family:system-ui,sans-serif;text-align:center;padding:48px">
<p><a style="color:#ff9a5a" href="en/">English</a> · <a style="color:#ff9a5a" href="es/">Español</a></p></body></html>""", encoding="utf-8")
(ROOT / "404.html").write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>404 · PortRace VI</title>
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"></head>
<body style="background:#0a0a0f;color:#f4f4f7;font-family:system-ui,sans-serif;text-align:center;padding:64px">
<h1>404</h1><p><a style="color:#ff9a5a" href="{BASE}/en/">English</a> · <a style="color:#ff9a5a" href="{BASE}/es/">Español</a></p></body></html>""", encoding="utf-8")

# carpeta limpia para publicar: solo lo necesario (sin src/, build.py, notas)
import shutil
PUB = ROOT / "public"
if PUB.exists(): shutil.rmtree(PUB)
PUB.mkdir()
for name in ("en", "es", "assets"):
    shutil.copytree(ROOT / name, PUB / name)
for name in ("index.html", "404.html", "robots.txt", "sitemap.xml", ".nojekyll"):
    shutil.copy(ROOT / name, PUB / name)
# archivos estáticos (p. ej. verificación de Search Console): a la raíz; los de Google también en /en/ y /es/
_static = ROOT / "src" / "static"
if _static.exists():
    for f in sorted(_static.iterdir()):
        if f.is_file():
            shutil.copy(f, PUB / f.name)
            if f.name.startswith("google"):
                for lg in ("en", "es"): shutil.copy(f, PUB / lg / f.name)

print(f"OK -> {ROOT} | base={BASE} | páginas: {2 + 2 * (len(GPUS) + 2)} + sitemap/robots")
