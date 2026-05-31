from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import psycopg2.extras
from database import get_conn
from utils.jwt import create_access_token, create_refresh_token
from utils.password import verify_password

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


def get_user_by_username(username: str) -> dict | None:
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT id, username, hashed_password FROM shopmind_users WHERE username = %s", (username,))
            row = cur.fetchone()
            return dict(row) if row else None
    finally:
        conn.close()


@router.post("/auth/login")
def login(req: LoginRequest):
    user = get_user_by_username(req.username)
    if not user or not verify_password(req.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {
        "access_token": create_access_token(user["username"]),
        "refresh_token": create_refresh_token(user["username"]),
        "token_type": "bearer",
    }
