from fastapi import FastAPI
from src.api.routes import health, alerts
from src.db.postgres import db
from src.db.redis import redis_client
from src.utils.logging import setup_logging

setup_logging()

app = FastAPI(
    title="AlertSentry-AI",
    description="AI-Powered SOC Alert Triage Assistant",
    version="0.1.0"
)

@app.on_event("startup")
async def startup():
    db.init()
    redis_client.init()

@app.on_event("shutdown")
async def shutdown():
    await db.close()
    await redis_client.close()

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(alerts.router, prefix="/api/v1", tags=["alerts"])
