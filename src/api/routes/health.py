from fastapi import APIRouter
from src.db.postgres import db
from src.db.redis import redis_client

router = APIRouter()


@router.get("/health")
async def health_check():
    # Check DB connection
    db_status = "ok"
    try:
        async with db.session_maker() as session:
            await session.execute("SELECT 1")
    except Exception:
        db_status = "error"

    # Check Redis connection
    redis_status = "ok"
    try:
        client = await redis_client.get_client()
        await client.ping()
    except Exception:
        redis_status = "error"

    return {
        "status": "ok" if db_status == "ok" and redis_status == "ok" else "error",
        "database": db_status,
        "redis": redis_status,
    }
