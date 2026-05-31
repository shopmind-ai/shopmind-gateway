import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from config import AGENT_URLS
from database import get_conn
from middleware.auth import require_auth

router = APIRouter()
_TIMEOUT = 10.0


def log_usage(username: str, agent_name: str, usage: dict):
    if not usage:
        return
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM shopmind_users WHERE username = %s", (username,))
            row = cur.fetchone()
            user_id = row[0] if row else None
            cur.execute(
                "INSERT INTO shopmind_usage_logs (user_id, agent_name, input_tokens, output_tokens) VALUES (%s,%s,%s,%s)",
                (user_id, agent_name, usage.get("input_tokens", 0), usage.get("output_tokens", 0)),
            )
        conn.commit()
    finally:
        conn.close()


@router.post("/api/v1/{agent}/invoke")
async def invoke(agent: str, request: Request, username: str = Depends(require_auth)):
    if agent not in AGENT_URLS:
        raise HTTPException(status_code=404, detail=f"Unknown agent: {agent}")

    body = await request.json()
    url = f"{AGENT_URLS[agent]}/invoke"

    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(url, json=body)
            data = resp.json()
            log_usage(username, agent, data.get("usage", {}))
            return JSONResponse(status_code=resp.status_code, content=data)
    except httpx.TimeoutException:
        return JSONResponse(
            status_code=503,
            content={"status": "degraded", "message": "服务暂时不可用，请稍后重试"},
        )


@router.get("/api/v1/{agent}/health")
async def health(agent: str, _: str = Depends(require_auth)):
    if agent not in AGENT_URLS:
        raise HTTPException(status_code=404, detail=f"Unknown agent: {agent}")

    url = f"{AGENT_URLS[agent]}/health"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url)
            return JSONResponse(status_code=resp.status_code, content=resp.json())
    except httpx.TimeoutException:
        return JSONResponse(status_code=503, content={"status": "unreachable"})
