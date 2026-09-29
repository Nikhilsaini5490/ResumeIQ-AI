import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.main import app
from app.services.sections import split_sections
from app.services.skills import extract_skills, flatten_skills
from app.services.matcher import MatchingService

client = TestClient(app)


def test_section_split():
    text = """Skills\nPython, SQL\n\nProjects\nBuilt a fraud detection system."""
    sections = split_sections(text)
    assert "skills" in sections
    assert "projects" in sections


def test_skill_extraction():
    text = "Python SQL Machine Learning FastAPI PyTorch GitHub Docker"
    skills = flatten_skills(extract_skills(text))
    assert "Python" in skills
    assert "SQL" in skills
    assert "Machine Learning" in skills
    assert "FastAPI" in skills


def test_tfidf_similarity():
    score = MatchingService.tfidf_similarity(
        "machine learning python data science",
        "python machine learning engineer",
    )
    assert 0 <= score <= 1


def test_analyze_file_rejects_unreadable_resume():
    response = client.post(
        "/analyze-file",
        files={"resume": ("resume.txt", b"", "text/plain")},
        data={"job_description": "A job description with enough detail."},
    )
    assert response.status_code == 400
    assert "enough text" in response.json()["detail"]


def test_analyze_file_rejects_short_job_description():
    response = client.post(
        "/analyze-file",
        files={"resume": ("resume.txt", b"Python developer with several years of experience.", "text/plain")},
        data={"job_description": "Short"},
    )
    assert response.status_code == 400
    assert "at least 20 characters" in response.json()["detail"]
