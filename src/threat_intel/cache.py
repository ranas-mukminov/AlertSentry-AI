import json
from typing import Optional, Any
from src.db.redis import get_redis
from src.utils.logging import get_logger

logger = get_logger(__name__)

class ThreatIntelCache:
    def __init__(self, ttl_seconds: int = 86400):  # Default 24h
        self.ttl = ttl_seconds

    async def get(self, key: str) -> Optional[Any]:
        try:
            redis = await get_redis()
            data = await redis.get(f"ti:{key}")
            if data:
                return json.loads(data)
        except Exception as e:
            logger.error(f"Error reading from cache: {e}")
        return None

    async def set(self, key: str, value: Any, ttl: int = None):
        try:
            redis = await get_redis()
            await redis.set(
                f"ti:{key}",
                json.dumps(value),
                ex=ttl or self.ttl
            )
        except Exception as e:
            logger.error(f"Error writing to cache: {e}")

ti_cache = ThreatIntelCache()
