"""Minimal FastAPI skeleton — real endpoints (risk scores, survival curves, agent) come later
per Design Spec §7. For now: prove the container runs and can reach Postgres.
"""
import os

import psycopg2
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Trial Retention Engine API")


@app.get("/health")
def health():
    """Liveness check — is the API process itself up, no external dependencies."""
    return {"status": "ok"}


@app.get("/db-health")
def db_health():
    """Readiness check — can the API actually reach Postgres, not just itself."""
    try:
        conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            port=os.environ.get("DB_PORT", "5432"),
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            dbname=os.environ["DB_NAME"],
        )
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            cur.fetchone()
        conn.close()
        return {"status": "ok", "db": "reachable"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"database unreachable: {exc}")
