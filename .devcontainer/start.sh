#!/usr/bin/env bash
set -euo pipefail

if ! curl --fail --silent http://127.0.0.1:8000/health >/dev/null; then
  nohup python -m uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000 >/tmp/resumeiq-api.log 2>&1 &
fi

if ! curl --fail --silent http://127.0.0.1:8501/_stcore/health >/dev/null; then
  nohup streamlit run frontend/app.py --server.address 0.0.0.0 --server.port 8501 >/tmp/resumeiq-streamlit.log 2>&1 &
fi