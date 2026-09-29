from __future__ import annotations
from app.services.sections import split_sections
from app.services.scoring import ScoringService
from app.services.recommendations import build_recommendations
from app.services.rag import ResumeRAG
from app.utils.text import normalize_whitespace


class ResumeAnalyzer:
    def analyze(self, resume_text: str, job_text: str) -> dict:
        resume_text = normalize_whitespace(resume_text)
        job_text = normalize_whitespace(job_text)
        sections = split_sections(resume_text)
        analysis = ScoringService.analyze(resume_text, sections, job_text)
        recommendations = build_recommendations(analysis, sections)
        return {
            "score": analysis.score,
            "breakdown": {
                "skill_match": analysis.skill_match,
                "semantic_match": analysis.semantic_match,
                "experience_match": analysis.experience_match,
                "project_match": analysis.project_match,
                "education_match": analysis.education_match,
            },
            "matched_skills": analysis.matched_skills,
            "missing_skills": analysis.missing_skills,
            "resume_skills": analysis.resume_skills,
            "job_skills": analysis.job_skills,
            "similarity": {
                "tfidf": analysis.tfidf_score,
                "embedding": analysis.embedding_score,
                "method_used": "transformer" if analysis.embedding_score is not None else "tfidf",
            },
            "sections": sections,
            "recommendations": recommendations,
        }
