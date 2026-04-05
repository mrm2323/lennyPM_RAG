import re
from pathlib import Path
from typing import Dict

FILLER_WORDS = [
    r"\bum\b",
    r"\buh\b",
    r"\byou know\b",
    r"\blike\b",
    r"\bi mean\b",
    r"\bso\b",
    r"\bright\b",
    r"\bwell\b",
    r"\bokay\b",
    r"\bactually\b",
    r"\bkind of\b",
    r"\bsort of\b",
]

FILLER_PATTERN = re.compile("|".join(FILLER_WORDS), flags=re.IGNORECASE)
TIMESTAMP_PATTERN = re.compile(r"\(?\[?\d{1,2}:\d{2}:\d{2}\]?\)?")
SPEAKER_LABEL_PATTERN = re.compile(r"^[A-Za-z0-9 ',-]+\s*\(\d{2}:\d{2}:\d{2}\):", flags=re.MULTILINE)


def clean_transcript_text(text: str) -> str:
    text = TIMESTAMP_PATTERN.sub("", text)
    text = SPEAKER_LABEL_PATTERN.sub("", text)
    text = FILLER_PATTERN.sub("", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_source_metadata(path: Path) -> Dict[str, str]:
    source_id = path.stem
    guest_names = [g.strip() for g in re.split(r"\s*\+\s*", source_id) if g.strip()]
    source_label = source_id
    return {
        "source_id": source_id,
        "guest_names": guest_names,
        "source_label": source_label,
        "source_path": str(path),
    }
