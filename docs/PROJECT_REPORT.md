# ResumeIQ — Project Report Starter

## Title
AI-Powered Resume Intelligence and Semantic Job Matching System Using NLP and Transformer Embeddings

## Abstract
ResumeIQ is an NLP-based system that analyzes a candidate resume against a target job description. The platform extracts resume text and sections, identifies skills using a curated skill taxonomy, computes lexical similarity using TF-IDF, computes semantic similarity using sentence-transformer embeddings when available, and combines these signals into an explainable Resume Match Score. It also identifies skill gaps and generates recommendations. An optional local LLM/RAG layer provides interview preparation using information retrieved from the candidate resume and target role.

## Problem Statement
Students and job seekers often compare resumes with job descriptions manually. This can miss semantic relationships, important skills, and role-specific gaps. The proposed system automates comparison while keeping the score explainable.

## Objectives
- Parse resume PDF/DOCX/TXT files.
- Extract useful resume sections.
- Extract technical/professional skills.
- Compare resume and job description using traditional and transformer NLP.
- Produce an explainable matching score.
- Identify missing skills.
- Generate actionable recommendations.
- Provide a retrieval-based interview assistant.

## Modules
1. Document parsing
2. NLP normalization
3. Section extraction
4. Skill extraction
5. TF-IDF similarity
6. Transformer embedding similarity
7. Explainable scoring
8. Skill-gap analysis
9. Recommendation engine
10. RAG interview assistant
11. FastAPI backend
12. Streamlit dashboard

## Scoring Model
Current project implementation:

- 40% skill match
- 30% semantic match
- 15% experience relevance
- 10% project relevance
- 5% education match

This is a project-defined metric, not an official ATS score.

## Evaluation Plan
Create a labelled set of resume/job-description pairs and compare:

- Keyword baseline
- TF-IDF similarity
- Transformer similarity

For skill extraction report precision, recall and F1. For matching scores compare system scores to human ratings using MAE/RMSE and correlation.

## Future Work
- learned ranking model trained on labelled match data
- multilingual skill/entity extraction
- named entity recognition for organizations/people/education
- cloud storage and authentication
- production vector database
- automatic resume rewriting with human approval
- dashboard analytics across many job descriptions

## Limitations
The current skill extraction uses a curated taxonomy and exact/alias matching. The score is not a real ATS score. Production deployment should add stronger entity recognition, security, authentication, document scanning safeguards and a larger labelled evaluation dataset.
