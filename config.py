import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-prod")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
DATABASE_URL = os.getenv("DATABASE_URL", "")

AGENT_URLS: dict[str, str] = {
    "cleaning":  os.getenv("AGENT_CLEANING_URL",  "http://localhost:8001"),
    "customer":  os.getenv("AGENT_CUSTOMER_URL",  "http://localhost:8002"),
    "media":     os.getenv("AGENT_MEDIA_URL",     "http://localhost:8003"),
    "social":    os.getenv("AGENT_SOCIAL_URL",    "http://localhost:8004"),
    "clip":      os.getenv("AGENT_CLIP_URL",      "http://localhost:8005"),
    "training":  os.getenv("AGENT_TRAINING_URL",  "http://localhost:8006"),
    "cluster":   os.getenv("AGENT_CLUSTER_URL",   "http://localhost:8007"),
    "finetune":  os.getenv("AGENT_FINETUNE_URL",  "http://localhost:8008"),
}
