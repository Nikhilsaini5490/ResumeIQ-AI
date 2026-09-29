import json
from pathlib import Path
from app.utils.text import normalize_for_match, unique_preserve

CATALOG_PATH = Path(__file__).resolve().parents[3] / "data" / "skills.json"


def load_catalog() -> dict:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def _contains_phrase(text: str, phrase: str) -> bool:
    normalized = normalize_for_match(text)
    target = normalize_for_match(phrase)
    if not target:
        return False
    # Word-aware match, allowing special chars in skill names.
    return f" {target} " in f" {normalized} "


def extract_skills(text: str) -> dict[str, list[str]]:
    catalog = load_catalog()
    found: dict[str, list[str]] = {}
    for category, skills in catalog.items():
        matches = []
        for skill, aliases in skills.items():
            candidates = [skill] + aliases
            if any(_contains_phrase(text, c) for c in candidates):
                matches.append(skill)
        if matches:
            found[category] = sorted(unique_preserve(matches), key=str.lower)
    return found


def flatten_skills(skill_map: dict[str, list[str]]) -> list[str]:
    result: list[str] = []
    for vals in skill_map.values():
        result.extend(vals)
    return sorted(unique_preserve(result), key=str.lower)
