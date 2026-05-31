from fastapi import APIRouter, Depends
import psycopg2.extras
from database import get_conn
from middleware.auth import require_auth

router = APIRouter()


def get_usage_summary() -> dict:
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT
                    agent_name,
                    SUM(input_tokens)  AS total_input,
                    SUM(output_tokens) AS total_output,
                    COUNT(*)           AS call_count
                FROM shopmind_usage_logs
                GROUP BY agent_name
                ORDER BY agent_name
            """)
            rows = cur.fetchall()
            return {"by_agent": [dict(r) for r in rows]}
    finally:
        conn.close()


@router.get("/api/v1/usage/summary")
def usage_summary(_: str = Depends(require_auth)):
    return get_usage_summary()
