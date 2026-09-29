from __future__ import annotations
from app.services.skills import flatten_skills


def build_recommendations(analysis, sections: dict[str, str]) -> list[str]:
    recs: list[str] = []
    if analysis.missing_skills:
        top = ", ".join(analysis.missing_skills[:6])
        recs.append(f"Prioritize the missing job skills: {top}.")
    if analysis.project_match < 70:
        recs.append("Rewrite project bullets to explicitly connect your work to the target role and measurable outcomes.")
    if analysis.experience_match < 70:
        recs.append("Strengthen experience bullets with tools used, responsibilities, and measurable results.")
    if analysis.semantic_match < 70:
        recs.append("Align the resume wording with the job description while keeping claims truthful and evidence-based.")
    if "skills" not in sections:
        recs.append("Add a dedicated technical skills section so important technologies are easy to find.")
    if len(analysis.matched_skills) < 3:
        recs.append("Add concrete project evidence for the most important skills instead of listing skills alone.")
    if not recs:
        recs.append("Your resume is broadly aligned. Focus on quantifying project impact and preparing role-specific interview stories.")
    return recs[:6]
