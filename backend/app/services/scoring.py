from __future__ import annotations
from dataclasses import dataclass

from app.services.matcher import MatchingService
from app.services.skills import extract_skills, flatten_skills


@dataclass
class MatchAnalysis:
    score: float
    skill_match: float
    semantic_match: float
    experience_match: float
    project_match: float
    education_match: float
    matched_skills: list[str]
    missing_skills: list[str]
    resume_skills: list[str]
    job_skills: list[str]
    tfidf_score: float
    embedding_score: float | None


class ScoringService:
    @staticmethod
    def skill_score(resume_skills: list[str], job_skills: list[str]) -> tuple[float, list[str], list[str]]:
        if not job_skills:
            return 0.0, [], []
        rset = {s.lower() for s in resume_skills}
        jset = {s.lower() for s in job_skills}
        matched = sorted([s for s in job_skills if s.lower() in rset], key=str.lower)
        missing = sorted([s for s in job_skills if s.lower() not in rset], key=str.lower)
        return len(matched) / len(jset), matched, missing

    @classmethod
    def analyze(cls, resume_text: str, sections: dict[str, str], job_text: str) -> MatchAnalysis:
        resume_skills_map = extract_skills(resume_text)
        job_skills_map = extract_skills(job_text)
        resume_skills = flatten_skills(resume_skills_map)
        job_skills = flatten_skills(job_skills_map)
        skill_match, matched, missing = cls.skill_score(resume_skills, job_skills)

        overall = MatchingService.compare(resume_text, job_text)
        exp = MatchingService.compare(sections.get("experience", ""), job_text).semantic_score if sections.get("experience") else overall.semantic_score * 0.8
        proj = MatchingService.compare(sections.get("projects", ""), job_text).semantic_score if sections.get("projects") else overall.semantic_score * 0.8
        edu_text = sections.get("education", "")
        education = 1.0 if any(k in edu_text.lower() for k in ["b.tech", "bachelor", "b.sc", "m.tech", "m.sc", "computer", "data science", "engineering"]) else 0.65

        score = (
            0.40 * skill_match +
            0.30 * overall.semantic_score +
            0.15 * exp +
            0.10 * proj +
            0.05 * education
        ) * 100

        return MatchAnalysis(
            score=round(score, 1),
            skill_match=round(skill_match * 100, 1),
            semantic_match=round(overall.semantic_score * 100, 1),
            experience_match=round(exp * 100, 1),
            project_match=round(proj * 100, 1),
            education_match=round(education * 100, 1),
            matched_skills=matched,
            missing_skills=missing,
            resume_skills=resume_skills,
            job_skills=job_skills,
            tfidf_score=round(overall.tfidf_score, 4),
            embedding_score=round(overall.embedding_score, 4) if overall.embedding_score is not None else None,
        )
