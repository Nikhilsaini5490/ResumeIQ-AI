# 10-Slide Class Presentation

## Slide 1 — Title
ResumeIQ: AI-Powered Resume Intelligence & Job Matching

## Slide 2 — Problem
Manual resume screening and job matching is time-consuming and keyword matching misses semantic relationships.

## Slide 3 — Objectives
Show the five core goals: extraction, matching, scoring, skill gaps, interview preparation.

## Slide 4 — Architecture
Resume → Parser → NLP → Skills → TF-IDF/Embeddings → Scoring → Recommendations → RAG Assistant.

## Slide 5 — NLP Pipeline
Tokenization/normalization → section extraction → skill extraction.

## Slide 6 — Matching
Compare keyword/TF-IDF baseline against sentence-transformer semantic similarity.

## Slide 7 — Explainable Score
Show the 40/30/15/10/5 scoring breakdown and explain that it is a project-defined metric.

## Slide 8 — Live Demo
Upload resume → paste JD → Analyze → inspect skills/gaps → ask interview question.

## Slide 9 — Evaluation
Show your measured precision/recall/F1 and matching error/correlation results once you have a labelled dataset.

## Slide 10 — Future Scope
Multilingual NLP, better NER, learned ranking, cloud deployment, production vector database.

## Viva Questions
1. Why TF-IDF?
2. Why transformer embeddings?
3. What is cosine similarity?
4. Why combine multiple signals?
5. How would you evaluate skill extraction?
6. What is RAG?
7. What are the limitations of a curated skill list?
8. How would you prevent hallucinations in an LLM assistant?
9. How would you scale the system?
10. What makes the score explainable?
