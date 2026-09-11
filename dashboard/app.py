"""Minimal Streamlit skeleton — the real coordinator dashboard (SHAP force plots, agent-drafted
briefs, per Design Spec §7) comes later. For now: prove the container runs and can reach the api
service.
"""
import os

import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://api:8000")

st.title("Trial Retention Engine — Dashboard")

st.write(f"Checking API at `{API_URL}`...")

try:
    health = requests.get(f"{API_URL}/health", timeout=5).json()
    db_health = requests.get(f"{API_URL}/db-health", timeout=5).json()
    st.success(f"API: {health}")
    st.success(f"Database (via API): {db_health}")
except requests.RequestException as exc:
    st.error(f"Could not reach API: {exc}")
