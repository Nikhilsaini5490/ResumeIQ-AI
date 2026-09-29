import re
from app.utils.text import normalize_whitespace

SECTION_ALIASES = {
    "summary": {"summary", "profile", "objective", "professional summary"},
    "education": {"education", "academic background", "qualifications"},
    "experience": {"experience", "work experience", "employment", "internship", "professional experience"},
    "projects": {"projects", "project experience", "academic projects"},
    "skills": {"skills", "technical skills", "core skills", "technologies"},
    "certifications": {"certifications", "certificates", "licenses"},
    "achievements": {"achievements", "awards", "accomplishments"},
}


def _canon_heading(line: str) -> str | None:
    clean = re.sub(r"[^a-zA-Z ]", " ", line).strip().lower()
    clean = normalize_whitespace(clean)
    for key, aliases in SECTION_ALIASES.items():
        if clean in aliases:
            return key
    return None


def split_sections(text: str) -> dict[str, str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    sections: dict[str, list[str]] = {k: [] for k in SECTION_ALIASES}
    current: str | None = None
    unknown: list[str] = []

    for line in lines:
        heading = _canon_heading(line)
        if heading:
            current = heading
            continue
        if current:
            sections[current].append(line)
        else:
            unknown.append(line)

    if unknown:
        sections["summary"] = unknown + sections["summary"]

    return {k: normalize_whitespace(" ".join(v)) for k, v in sections.items() if v}
