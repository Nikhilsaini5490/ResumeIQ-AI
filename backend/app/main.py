from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from app.config import get_settings
from app.services.analyzer import ResumeAnalyzer
from app.services.parser import DocumentParser
from app.services.rag import ResumeRAG

app = FastAPI(title="ResumeIQ API", version="1.0.0")
_analyzer = ResumeAnalyzer()


class AnalyzeRequest(BaseModel):
    resume_text: str = Field(min_length=20)
    job_description: str = Field(min_length=20)


class QuestionRequest(BaseModel):
    resume_text: str = Field(min_length=20)
    job_description: str = Field(min_length=20)
    question: str = Field(min_length=3)


def _validate_text_size(label: str, text: str) -> None:
    max_chars = get_settings().max_text_chars
    if len(text) > max_chars:
        raise HTTPException(
            status_code=413,
            detail=f"{label} exceeds the configured limit of {max_chars} characters.",
        )


@app.get("/")
def root():
    s = get_settings()
    return {
        "name": "ResumeIQ API",
        "status": "ok",
        "embeddings_enabled": s.use_embeddings,
        "ollama_enabled": s.use_ollama,
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    _validate_text_size("Resume text", request.resume_text)
    _validate_text_size("Job description", request.job_description)
    try:
        return _analyzer.analyze(request.resume_text, request.job_description)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/analyze-file")
async def analyze_file(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
    try:
        data = await resume.read()
        text = DocumentParser.parse_bytes(resume.filename or "resume.txt", data)
        _validate_text_size("Resume text", text)
        _validate_text_size("Job description", job_description)
        if len(text.strip()) < 20:
            raise HTTPException(
                status_code=400,
                detail="Could not extract enough text from the resume. Please upload a readable document.",
            )
        if len(job_description.strip()) < 20:
            raise HTTPException(
                status_code=400,
                detail="Job description must contain at least 20 characters.",
            )
        return _analyzer.analyze(text, job_description)
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/ask")
def ask(request: QuestionRequest):
    _validate_text_size("Resume text", request.resume_text)
    _validate_text_size("Job description", request.job_description)
    _validate_text_size("Question", request.question)
    try:
        rag = ResumeRAG(request.resume_text, request.job_description)
        return {"answer": rag.answer(request.question), "question": request.question}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
