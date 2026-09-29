# ResumeIQ

[![CI](https://github.com/Nikhilsaini5490/ResumeIQ-AI/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Nikhilsaini5490/ResumeIQ-AI/actions/workflows/ci.yml)

ResumeIQ compares a resume with a job description and reports an explainable match score, skill gaps, and interview-preparation suggestions. It uses a Streamlit interface and a FastAPI backend.

The score is a project-defined metric, not an official ATS score or a hiring recommendation.

## Features

- Parse PDF, DOCX, TXT, and Markdown resumes.
- Identify resume sections and catalogued skills.
- Compare documents with TF-IDF and optional sentence-transformer embeddings.
- Show a weighted score breakdown, matched skills, skill gaps, and recommendations.
- Retrieve resume and job-description context for interview questions, with an optional Ollama integration.
- Export analysis results as JSON.

## Project layout

```text
backend/       FastAPI API and analysis services
data/          Skill taxonomy
docs/          Project report and presentation outline
frontend/      Streamlit dashboard
tests/         Automated tests
.devcontainer/ GitHub Codespaces setup
```

## Run locally on Windows

Use Python 3.11. From the repository root, create an environment and install dependencies:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Start the API in one terminal:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --reload --port 8000
```

Start the dashboard in a second terminal:

```powershell
.\.venv\Scripts\python.exe -m streamlit run frontend/app.py
```

Open the dashboard at `http://127.0.0.1:8501` and the API documentation at `http://127.0.0.1:8000/docs`.

If PowerShell blocks virtual-environment activation, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`, then activate again.

## Run with Docker Compose

With Docker Desktop running:

```powershell
docker compose up --build
```

Open `http://127.0.0.1:8501`. The frontend waits for the backend health check before starting.

## Run in GitHub Codespaces

On the repository page, choose **Code**, then **Codespaces**, then **Create codespace on main**. The dev container installs the non-transformer dependencies, starts both services, and forwards ports 8000 and 8501. Open the forwarded **ResumeIQ Dashboard** port. Codespaces usage is subject to the account's GitHub plan and billing settings.

Codespaces uses TF-IDF by default to avoid downloading a transformer model. The local and Docker configurations can use embeddings when enabled.

## Configuration

Copy `.env.example` to `.env` in the repository root to customize settings.

| Variable | Default | Purpose |
| --- | --- | --- |
| `USE_EMBEDDINGS` | `true` | Enable sentence-transformer similarity. The model may download on first use. |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence-transformer model name. |
| `USE_OLLAMA` | `false` | Enable the optional Ollama interview assistant. |
| `OLLAMA_URL` | `http://127.0.0.1:11434/api/generate` | Ollama generation endpoint. |
| `OLLAMA_MODEL` | `llama3.2` | Ollama model name. |
| `MAX_TEXT_CHARS` | `20000` | Maximum length for each resume, job-description, or question input. |

When embeddings are disabled or unavailable, matching falls back to TF-IDF. The interview assistant also has a deterministic fallback when Ollama is disabled or unavailable.

## API

- `GET /health` reports API health.
- `POST /analyze` accepts resume and job-description text as JSON.
- `POST /analyze-file` accepts a resume upload and job description as multipart form data.
- `POST /ask` retrieves relevant context and answers an interview-preparation question.

Interactive request schemas are available at `/docs` when the API is running.

## Tests

The tests use the TF-IDF path and do not require a model download:

```powershell
$env:USE_EMBEDDINGS = "false"
.\.venv\Scripts\python.exe -m pytest -q
```

GitHub Actions runs the test suite on pushes and pull requests to `main`.

## Privacy and limitations

- The API does not write uploaded resumes to a database or disk. The dashboard keeps the returned analysis in the user's Streamlit session.
- The optional Ollama integration sends retrieved context to the configured Ollama endpoint. Use only endpoints you trust.
- ResumeIQ is a prototype. Review the scoring logic and privacy requirements before using it with real candidate data or making employment decisions.
- No license has been selected for this repository. Add a license before granting others reuse rights.
