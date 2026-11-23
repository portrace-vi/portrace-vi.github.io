# PortRace VI

Unofficial tracker of the community projects trying to run **GTA VI on PC**, with an estimated release window in days and a PC compatibility check. Bilingual: English and Spanish.

Tracker no oficial de los proyectos comunitarios que intentan correr **GTA VI en PC**, con una estimación en días y un verificador de compatibilidad de PC. En español e inglés.

## What it is / Qué es

- **Race tracker:** milestones per project, each with evidence and its source type. Stars, commits, README changes and takedowns are checked by a watcher every 30 minutes.
- **PC check:** estimates your tier from GPU, CPU, RAM and storage. It is a lookup table, **not a benchmark**: it does not measure your hardware.
- **Estimates in days:** a pace-based model with visible assumptions in `src/data.json`. An editorial estimate, not a promise.

## What it is not / Qué no es

- Not affiliated with Rockstar Games or Take-Two Interactive.
- It hosts and links **no** game files, builds, keys or leaker channels, and never will.
- It does not run any project's code.

## Structure

```
src/data.json            tracker data, evidence, events, estimates (source of truth)
src/gpus.json cpus.json  hardware tables for the PC check
src/readme-hashes.json   state used by the watcher to detect README changes
tools/watch.py           watcher (GitHub API)
build.py                 generates public/ (static site, /en/ and /es/)
.github/workflows/       watcher + build + deploy to GitHub Pages
```

## Run locally

```bash
python3 tools/watch.py
python3 build.py --base http://localhost:8000
cd public && python3 -m http.server 8000
```

See [CONTRIBUTING.md](CONTRIBUTING.md). Code under the MIT license.
