# ResumeIQ — AI-Powered Resume Intelligence & Job Matching

A placement-ready NLP project for analyzing a resume against a job description.
It combines classic NLP, transformer embeddings, explainable scoring, skill-gap analysis, and an optional local LLM/RAG interview assistant.

## What this project does

1. Upload a PDF/DOCX/TXT resume.
2. Extract text and identify resume sections.
3. Extract technical and professional skills.
4. Enter or paste a job description.
5. Compare resume and job description with:
   - keyword/skill overlap
   - TF-IDF cosine similarity
   - transformer sentence embeddings (optional but recommended)
6. Produce an explainable Resume Match Score.
7. Show matched skills and skill gaps.
8. Analyze project/experience relevance.
9. Generate improvement suggestions.
10. Run a lightweight RAG-style interview assistant from the resume + job description.
11. Export the analysis as JSON.

## Architecture

```text
Resume PDF/DOCX/TXT
        |
        v
+-------------------+
| Document Parser   |
+-------------------+
        |
        v
+-------------------+
| NLP Preprocessing |
+-------------------+
        |
        +------------------+
        |                  |
        v                  v
  Section Split      Skill Extraction
        |                  |
        +--------+---------+
                 |
                 v
        +----------------+
        | Matching Engine |
        +----------------+
          /       |       \
         /        |        \
        v         v         v
    TF-IDF   Embeddings   Skill Match
       \         |          /
        \        |         /
         +-------+--------+
                 |
                 v
        +----------------+
        | Explainable    |
        | Scoring Engine |
        +----------------+
                 |
        +---------+---------+
        |         |         |
        v         v         v
      Score    Skill Gaps  Suggestions
                 |
                 v
          RAG Interview QA
                 |
                 v
            Streamlit UI
```

## Recommended environment

- Windows 10/11
- Python 3.11 recommended
- Visual Studio Code
- 8 GB RAM minimum; 16 GB is more comfortable
- Internet connection for the first download of the sentence-transformer model

## 1. Open the project in VS Code

Extract the ZIP, then open the `ResumeIQ` folder in VS Code.

Open the VS Code terminal and run:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again.

## 2. Run the backend

From the project root:

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Open:

`http://127.0.0.1:8000/docs`

You should see the FastAPI Swagger documentation.

## 3. Run the frontend

Open a second VS Code terminal in the project root:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run frontend/app.py
```

The browser will open the ResumeIQ dashboard.

## 4. Optional: enable transformer embeddings

Embeddings are enabled by default. The first analysis downloads the model:

`sentence-transformers/all-MiniLM-L6-v2`

If you have a machine without internet, the project automatically falls back to TF-IDF when embedding loading fails.

You can also force TF-IDF only by creating a `.env` file:

```env
USE_EMBEDDINGS=false
```

## 5. Optional: enable local LLM interview assistant

The project can work completely without an LLM. For a stronger demo, install Ollama separately and make a local model available, then set:

```env
USE_OLLAMA=true
OLLAMA_URL=http://127.0.0.1:11434/api/generate
OLLAMA_MODEL=llama3.2
```

When Ollama is unavailable, the system uses a deterministic fallback interview generator, so the main application still runs.

## 6. How to demo it in class

1. Upload a resume.
2. Paste a Data Scientist / ML Engineer job description.
3. Click **Analyze Resume**.
4. Show the overall match score.
5. Show matched and missing skills.
6. Compare TF-IDF and transformer semantic similarity.
7. Show why the score was assigned.
8. Show personalized recommendations.
9. Open the interview assistant and ask:
   - What can I be asked about my projects?
   - What skills am I missing?
   - What should I prepare for this job?

## 7. Suggested academic contribution

For your report, evaluate the system with a small labelled dataset of resume/job-description pairs. Compare:

- keyword matching
- TF-IDF cosine similarity
- transformer embedding similarity

For skill extraction evaluate precision, recall and F1-score. For matching scores, compare model scores to human annotations.

## 8. Important project limitation

The Resume Match Score is a project-defined metric, not an official ATS score. It should be described as an explainable matching score in your report and presentation.

## 9. Resume bullet after you actually build/evaluate it

- Built ResumeIQ, an NLP-based resume intelligence platform using TF-IDF, transformer embeddings, skill extraction, FastAPI, and an explainable job-matching pipeline with personalized skill-gap and interview recommendations.

Add numerical performance claims only after you measure them on your own evaluation dataset.

## Run in GitHub Codespaces

Open this repository in a Codespace. The development container installs the application dependencies, starts the FastAPI backend and Streamlit dashboard, and forwards ports 8000 and 8501. Open the forwarded port labeled **ResumeIQ Dashboard** to use the app. Transformer embeddings are disabled in the Codespace by default; the app uses TF-IDF and does not download a model.
