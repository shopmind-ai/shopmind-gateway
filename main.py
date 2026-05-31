from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.startup import check_and_init
from routers import auth, proxy, usage

app = FastAPI(title="ShopMind Gateway", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    check_and_init()


app.include_router(auth.router)
app.include_router(proxy.router)
app.include_router(usage.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "shopmind-gateway"}
