import json
import os
import requests
import streamlit as st

st.set_page_config(page_title="ResumeIQ", page_icon="📄", layout="wide")

API_URL = st.sidebar.text_input("Backend URL", os.getenv("RESUMEIQ_API", "http://127.0.0.1:8000"))

st.markdown("# 📄 ResumeIQ")
st.caption("NLP + transformer embeddings + explainable job matching + interview assistant")

with st.sidebar:
    st.markdown("### How to use")
    st.write("1. Upload a resume")
    st.write("2. Paste a job description")
    st.write("3. Analyze")
    st.write("4. Review gaps and recommendations")
    st.write("5. Ask the interview assistant")

left, right = st.columns([1, 1])
with left:
    uploaded = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt", "md"])
with right:
    jd = st.text_area(
        "Job Description",
        value=st.session_state.get("jd", ""),
        height=220,
        placeholder="Paste the complete job description here...",
    )

sample_jd = """Data Scientist / ML Engineer\n\nWe are looking for a candidate with Python, SQL, machine learning, NLP, PyTorch, Pandas, FastAPI, Git, Docker and AWS. The role involves building predictive models, evaluating experiments, developing REST APIs and communicating results."""

if st.button("Use sample job description"):
    st.session_state["jd"] = sample_jd
    st.rerun()

if "jd" in st.session_state and not jd:
    jd = st.session_state["jd"]

if uploaded:
    st.success(f"Loaded: {uploaded.name}")

if st.button("🚀 Analyze Resume", type="primary", disabled=(uploaded is None or not jd.strip())):
    with st.spinner("Extracting, matching and scoring..."):
        try:
            response = requests.post(
                f"{API_URL}/analyze-file",
                files={"resume": (uploaded.name, uploaded.getvalue(), uploaded.type or "application/octet-stream")},
                data={"job_description": jd},
                timeout=180,
            )
            response.raise_for_status()
            st.session_state["analysis"] = response.json()
            st.session_state["resume_text_for_qa"] = ""
        except Exception as exc:
            st.error(f"Backend error: {exc}")

analysis = st.session_state.get("analysis")

if analysis:
    st.divider()
    st.subheader("Match Overview")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Overall", f"{analysis['score']}%")
    c2.metric("Skills", f"{analysis['breakdown']['skill_match']}%")
    c3.metric("Semantic", f"{analysis['breakdown']['semantic_match']}%")
    c4.metric("Experience", f"{analysis['breakdown']['experience_match']}%")
    c5.metric("Projects", f"{analysis['breakdown']['project_match']}%")

    st.progress(min(max(analysis["score"] / 100, 0), 1), text=f"Resume Match Score: {analysis['score']}%")

    a, b = st.columns(2)
    with a:
        st.markdown("### ✅ Matched Skills")
        if analysis["matched_skills"]:
            st.write(", ".join(analysis["matched_skills"]))
        else:
            st.info("No catalogued skills matched.")
    with b:
        st.markdown("### ⚠️ Skill Gaps")
        if analysis["missing_skills"]:
            st.write(", ".join(analysis["missing_skills"]))
        else:
            st.success("No catalogued skill gaps detected.")

    st.markdown("### 📊 Similarity Methods")
    s1, s2, s3 = st.columns(3)
    s1.metric("TF-IDF", f"{analysis['similarity']['tfidf']:.3f}")
    emb = analysis["similarity"]["embedding"]
    s2.metric("Transformer", "Unavailable" if emb is None else f"{emb:.3f}")
    s3.metric("Selected", analysis["similarity"]["method_used"])

    st.markdown("### 💡 Recommendations")
    for rec in analysis["recommendations"]:
        st.write(f"• {rec}")

    with st.expander("Resume sections extracted"):
        for name, content in analysis["sections"].items():
            st.markdown(f"**{name.title()}**")
            st.write(content)

    st.download_button(
        "Download analysis JSON",
        data=json.dumps(analysis, indent=2),
        file_name="resumeiq_analysis.json",
        mime="application/json",
    )

st.divider()
st.subheader("🎯 Interview Assistant")
st.caption("Ask questions about the uploaded resume and target role. The backend uses retrieval plus an optional local LLM.")
question = st.text_input("Ask a question", placeholder="What interview questions should I prepare for this role?")

if st.button("Ask Interview Assistant", disabled=(uploaded is None or not jd.strip() or not question.strip())):
    with st.spinner("Retrieving relevant resume/job context..."):
        try:
            # Reuse parsed text through the analyze-file endpoint if analysis is not already available.
            # The API currently stores no session state, so send the file again for QA context.
            parsed = requests.post(
                f"{API_URL}/analyze-file",
                files={"resume": (uploaded.name, uploaded.getvalue(), uploaded.type or "application/octet-stream")},
                data={"job_description": jd},
                timeout=180,
            )
            parsed.raise_for_status()
            sections = parsed.json().get("sections", {})
            resume_text = " ".join(sections.values())
            response = requests.post(
                f"{API_URL}/ask",
                json={"resume_text": resume_text, "job_description": jd, "question": question},
                timeout=180,
            )
            response.raise_for_status()
            st.markdown("### Answer")
            st.write(response.json()["answer"])
        except Exception as exc:
            st.error(f"Assistant error: {exc}")
