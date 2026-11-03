"""Shared hallucination-filter and confidence helpers for the transcribe scripts.

Imported by merge_tracks.py (Path A multi-track) and split_merged.py (Path B
single merged track) to deduplicate the cleanup logic. Not a stand-alone CLI.
"""
import re

LOW_CONF_THRESHOLD = 0.5

# Known WhisperX silence-hallucination patterns (YouTube/subtitle training).
HALLUCINATION_PATTERNS = [
    re.compile(r"Subt[íi]tulos?\s+(?:realizados|creados|hechos|generados|por)\s+(?:por\s+)?la\s+comunidad\s+de\s+Amara\.org", re.IGNORECASE),
    re.compile(r"Subt[íi]tulos?\s+(?:por|de)\s+Subtitle\s+Workshop", re.IGNORECASE),
    re.compile(r"Subtitulad[oa]s?\s+por\s+Accesibilidad\s+TVE", re.IGNORECASE),
    re.compile(r"Suscr[íi]bete\s+al\s+canal", re.IGNORECASE),
    re.compile(r"Gracias\s+por\s+ver\s+(?:el\s+)?v[íi]deo", re.IGNORECASE),
    re.compile(r"S[íi](?:ga|gue)nos\s+en\s+(?:redes|facebook|twitter|instagram)", re.IGNORECASE),
    re.compile(r"\b(?:Like|Dale)\s+y\s+suscr[íi]bete", re.IGNORECASE),
]

SINGLE_CHAR_CASCADE = re.compile(r"^\W*([A-Za-zÀ-ÿ])(?:[\s,.]+\1){4,}[\s,.!?¿¡]*$")
NUM_SEQUENCE = re.compile(r"^(?:\d+[,.]?\s+){8,}\d+[.!?,]?\s*$")


def collapse_char_repeats(text):
    """Collapse runs of repeated characters or short units (e.g. 'Mialeeeeee'
    -> 'Miale', 'Jajajajajaja' -> 'Ja'). Returns (collapsed, was_modified)."""
    original = text
    text = re.sub(r"(.)\1{4,}", r"\1", text)
    text = re.sub(r"(?i)(.{2})\1{3,}", r"\1", text)
    return text, text != original


def detect_token_loop(text):
    """Collapse token-level repetition (unit repeats 3+ times) to a single unit."""
    tokens = text.split()
    n = len(tokens)
    if n < 6:
        return text
    for period in range(1, n // 3 + 1):
        unit = tokens[:period]
        reps = 0
        i = 0
        while i + period <= n and tokens[i:i + period] == unit:
            reps += 1
            i += period
        if reps >= 3 and i >= n - period:
            return " ".join(unit)
    return text


def clean_text(text):
    """Apply hallucination/loop cleanup. Return cleaned text, or None to drop."""
    text = (text or "").strip()
    if not text:
        return None
    if SINGLE_CHAR_CASCADE.match(text):
        return None
    if NUM_SEQUENCE.match(text):
        return None
    for p in HALLUCINATION_PATTERNS:
        if p.search(text):
            return None
    text = detect_token_loop(text)
    text, char_modified = collapse_char_repeats(text)
    if char_modified and len(text.strip()) < 4:
        return None
    return text.strip() or None


def avg_confidence(words):
    scores = [w.get("score") for w in words if w.get("word") and w.get("score") is not None]
    if not scores:
        return None
    return sum(scores) / len(scores)


def conf_marker(conf):
    """Return ' ~0.XX' if below threshold, else empty string."""
    if conf is not None and conf < LOW_CONF_THRESHOLD:
        return f" ~{conf:.2f}"
    return ""
