from fastapi import FastAPI
from src.api.agent import router as agent_router

app = FastAPI(title="Eletric Lab API", version="0.3.0")
app.include_router(agent_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
