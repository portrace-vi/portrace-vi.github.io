"""Detección de líneas de estado en un README (para avisar de cambios que importan).

signals(text)          -> líneas del README que hablan de estado (arranca, jugable, fps, pantalla negra...)
positive_playable(line) -> True si una línea parece afirmar que ALGO ya es jugable (para marcar prioridad)

Es heurístico: sirve para llamar la atención de una persona, no para decidir estados. Siempre se revisa a mano.
"""
import re

SIGNAL = re.compile(
    r"playable|\bboots?\b|title screen|main menu|in-?game|gameplay|\bfps\b|"
    r"black (screen|picture|frame)|device (lost|removal)|gpu (hang|fail)|"
    r"start-?up|frame rate|from pe entry", re.I)

_NEGATIVE = re.compile(r"❌|\bno\b|\bnot\b|n't|\byet\b|\bnever\b|pending|todo|planned|missing|fail|unverified", re.I)
_TOPIC = re.compile(r"playable|gameplay|story mode|in-?game", re.I)
_POSITIVE = re.compile(
    r"✅|\bworks?\b|\bworking\b|\byes\b|\bnow\b|\bavailable\b|\brunning\b|\breaches\b|\bplays\b|"
    r"\b(is|are) (fully |already )?playable\b|\bfully playable\b", re.I)


def _clean(line: str) -> str:
    l = line.replace("|", " ").replace("*", "").replace("`", "")
    l = re.sub(r"^[\s#>\-]+", "", l)
    return re.sub(r"\s+", " ", l).strip()


def signals(text: str, limit: int = 40):
    out = []
    for line in text.splitlines():
        l = _clean(line)
        if len(l) >= 12 and SIGNAL.search(l):
            l = l[:240]
            if l not in out:
                out.append(l)
    return out[:limit]


def positive_playable(line: str) -> bool:
    if not _TOPIC.search(line) or _NEGATIVE.search(line):
        return False
    return bool(_POSITIVE.search(line))
