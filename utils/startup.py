import psycopg2
from config import DATABASE_URL

DDL = """
CREATE TABLE IF NOT EXISTS shopmind_users (
    id              SERIAL PRIMARY KEY,
    username        VARCHAR(50)  UNIQUE NOT NULL,
    email           VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS shopmind_usage_logs (
    id            SERIAL PRIMARY KEY,
    user_id       INTEGER REFERENCES shopmind_users(id),
    agent_name    VARCHAR(50) NOT NULL,
    input_tokens  INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);
"""


def check_and_init():
    from utils.password import hash_password
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            cur.execute(DDL)
            cur.execute("SELECT COUNT(*) FROM shopmind_users")
            if cur.fetchone()[0] == 0:
                cur.execute(
                    "INSERT INTO shopmind_users (username, email, hashed_password) VALUES (%s, %s, %s)",
                    ("demo", "demo@shopmind.ai", hash_password("shopmind2026")),
                )
                print("[startup] Demo user created: demo / shopmind2026")
        conn.commit()
        print("[startup] Gateway DB initialized.")
    finally:
        conn.close()
