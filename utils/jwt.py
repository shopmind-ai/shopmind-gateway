from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

_ALGORITHM = "HS256"


def create_access_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {"sub": username, "type": "access", "exp": expire},
        SECRET_KEY, algorithm=_ALGORITHM,
    )


def create_refresh_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return jwt.encode(
        {"sub": username, "type": "refresh", "exp": expire},
        SECRET_KEY, algorithm=_ALGORITHM,
    )


def verify_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[_ALGORITHM])
    except JWTError:
        return None
