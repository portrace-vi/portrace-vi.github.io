#!/usr/bin/env python3
"""Vigilante de los repos seguidos (corre cada 30 min en GitHub Actions, o a mano).

Qué hace:
  1. Lee de la API pública de GitHub: estrellas, último push, commits, releases, y el README de cada repo.
  2. Detecta CAMBIOS: README modificado, release nuevo, repo no disponible (posible DMCA/takedown).
  3. Escribe src/snapshot.json (datos frescos para la web; no se versiona) y src/readme-hashes.json
     (estado persistente; solo cambia cuando algo cambia) y changes.md (resumen para abrir un issue).

No decide los estados del tracker: eso lo revisa una persona en src/data.json, con evidencia.
Token: usa GITHUB_TOKEN / GH_TOKEN si existe, o el de `gh auth token` si estás logueado. Nunca se imprime.
"""
import datetime, hashlib, json, os, pathlib, re, subprocess, sys, urllib.error, urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from signals import signals, positive_playable

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.load(open(ROOT / "src/data.json", encoding="utf-8"))
HASHES_F, SNAP_F, CHANGES_F = ROOT / "src/readme-hashes.json", ROOT / "src/snapshot.json", ROOT / "changes.md"
TITLE_F = ROOT / "changes.title"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def token():
    t = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if t: return t
    try:
        return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=10).stdout.strip() or None
    except Exception:
        return None
TOKEN = token()

def api(path, raw=False):
    h = {"Accept": "application/vnd.github.raw" if raw else "application/vnd.github+json", "User-Agent": "portrace-watch"}
    if TOKEN: h["Authorization"] = "Bearer " + TOKEN
    try:
        with urllib.request.urlopen(urllib.request.Request("https://api.github.com" + path, headers=h), timeout=25) as r:
            return r.status, r.read(), r.headers
    except urllib.error.HTTPError as e:
        return e.code, b"", e.headers
    except Exception:
        return 0, b"", {}

old = json.load(open(HASHES_F, encoding="utf-8")) if HASHES_F.exists() else {}
new_hashes, snap, changes, priority = {}, {}, [], []

for p in DATA["projects"]:
    slug = p.get("github")
    if not slug: continue
    prev = old.get(slug)
    code, body, _ = api(f"/repos/{slug}")
    if code in (404, 410, 451):   # 451 = Unavailable For Legal Reasons (típico de un DMCA)
        snap[slug] = {"unavailable": code, "fetched_at": NOW}
        new_hashes[slug] = prev or {}
        if not (prev or {}).get("unavailable"):
            changes.append(f"- **{p['name']}** (`{slug}`): the repository is now unavailable (HTTP {code}). Cause unknown: move, deletion, privacy change or takedown. Check manually and update the tracker.")
        new_hashes[slug] = {**(prev or {}), "unavailable": code}
        continue
    if code != 200:               # límite de API, red caída, etc.: no tocamos nada
        print(f"[watch] {slug}: HTTP {code}, se conserva el estado anterior", file=sys.stderr)
        if prev: new_hashes[slug] = prev
        continue
    repo = json.loads(body)
    if prev and prev.get("unavailable"):   # volvió a estar disponible
        priority.append(p["name"])
        changes.append(f"- **{p['name']}** (`{slug}`): 🚨 the repository is available again: https://github.com/{slug}")
    _, rb, _ = api(f"/repos/{slug}/readme", raw=True)
    sha = hashlib.sha256(rb).hexdigest() if rb else (prev or {}).get("sha")
    sig = signals(rb.decode("utf-8", "replace")) if rb else (prev or {}).get("signals")
    cc, cb, ch = api(f"/repos/{slug}/commits?per_page=1")
    commits, last = None, None
    if cc == 200:
        arr = json.loads(cb)
        m = re.search(r'[?&]page=(\d+)>; rel="last"', ch.get("Link", "") if hasattr(ch, "get") else "")
        commits = int(m.group(1)) if m else len(arr)
        if arr:
            c0 = arr[0]
            last = {"sha": c0["sha"][:7], "message": c0["commit"]["message"].split("\n")[0][:140], "date": c0["commit"]["committer"]["date"]}
    rc, rl, _ = api(f"/repos/{slug}/releases?per_page=5")
    releases = [r["tag_name"] for r in json.loads(rl)] if rc == 200 else (prev or {}).get("releases", [])

    changed_at, baseline = (prev or {}).get("changed_at", NOW), (prev or {}).get("baseline", True)
    if prev is None:
        changed_at, baseline = NOW, True                           # primera vez que lo vemos: línea base
    else:
        if sha and prev.get("sha") and sha != prev["sha"]:
            changed_at, baseline = NOW, False
            detail, old_sig = "", prev.get("signals")
            if old_sig is not None and sig is not None:     # qué líneas de estado cambiaron
                added = [l for l in sig if l not in old_sig]; removed = [l for l in old_sig if l not in sig]
                detail = "".join(f"\n  - ➕ {l}" for l in added[:6]) + "".join(f"\n  - ➖ {l}" for l in removed[:6])
                if any(positive_playable(l) for l in added): priority.append(p["name"])
            changes.append(f"- **{p['name']}** (`{slug}`): README changed. Review the diff: https://github.com/{slug}/commits/{repo.get('default_branch','main')}/README.md . "
                           f"The tracker status was last checked on {p['checked']['date']}.{detail}")
        for tag in releases:
            if tag not in prev.get("releases", []):
                priority.append(p["name"])
                changes.append(f"- **{p['name']}** (`{slug}`): 🚨 new release `{tag}` https://github.com/{slug}/releases/tag/{tag}")
    new_hashes[slug] = {"sha": sha, "changed_at": changed_at, "baseline": baseline, "releases": releases, "signals": sig}
    snap[slug] = {"stars": repo["stargazers_count"], "pushed_at": repo["pushed_at"], "open_issues": repo["open_issues_count"],
                  "archived": repo["archived"], "commits": commits, "last_commit": last, "releases": releases[:3],
                  "readme_changed_at": changed_at, "readme_baseline": baseline, "fetched_at": NOW}

SNAP_F.write_text(json.dumps({"fetched_at": NOW, "repos": snap}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
if json.dumps(new_hashes, sort_keys=True) != json.dumps(old, sort_keys=True):
    HASHES_F.write_text(json.dumps(new_hashes, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
if priority:
    names = ", ".join(sorted(set(priority)))
    changes.insert(0, f"🚨 **Priority: possible playable build or new release in: {names}.** Check it first and update `src/data.json` if it is real.\n")
    TITLE_F.write_text(f"🚨 Possible playable build or new release: {names}", encoding="utf-8")
elif changes:
    TITLE_F.write_text(f"Tracked repos changed ({NOW[:10]})", encoding="utf-8")
CHANGES_F.write_text("\n".join(changes) + ("\n" if changes else ""), encoding="utf-8")
print(f"[watch] {len(snap)} repos | cambios: {len(changes)}")
for c in changes: print(c)
