# Contributing / Contribuir

PortRace VI is an unofficial, independent tracker of community projects trying to run GTA VI on PC.
PortRace VI es un tracker independiente y no oficial de proyectos comunitarios que intentan correr GTA VI en PC.

## Corrections / Correcciones

The most useful contribution is a **correction with a source**. Open an issue with:

1. What is wrong (project, milestone, number).
2. A link to the evidence: the project's own README, a commit, a release, a test log or a screenshot.

Un estado solo cambia a "hecho" si hay evidencia. Sin evidencia, es "aún no".

Status data lives in `src/data.json`. Every status needs an entry in that project's `evidence` list, tagged `readme`, `inferred`, `discord` (relayed, unverified) or `press`.

## Hard rules / Reglas duras

- **No game files, builds, keys, dumps or download links.** Not in code, issues or pull requests.
- **No links to leakers, their channels or tokens.** Press coverage with sources is fine.
- No official logos, art, screenshots or audio from the game.
- No claims that something is playable without evidence from the project itself.
- Do not post private logs or personal data.

## Build

```bash
python3 tools/watch.py        # optional: refresh GitHub data (uses `gh auth token` if logged in)
python3 build.py --base http://localhost:8000
cd public && python3 -m http.server 8000
```

Python 3.10+ and no third-party packages are needed.

## Takedowns / Retiros

If a rights holder asks for content to be removed, open an issue or contact the maintainers and it will be handled promptly.
