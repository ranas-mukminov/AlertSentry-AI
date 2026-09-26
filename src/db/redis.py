import redis.asyncio as redis
from src.config import get_config
from typing import Optional


class RedisClient:
    def __init__(self):
        self.client: Optional[redis.Redis] = None

    def init(self):
        config = get_config()
        redis_config = config.database.redis

        self.client = redis.Redis(
            host=redis_config["host"],
            port=redis_config["port"],
            decode_responses=True,
            encoding="utf-8",
        )

    async def get_client(self) -> redis.Redis:
        if self.client is None:
            self.init()
        return self.client

    async def close(self):
        if self.client:
            await self.client.close()


redis_client = RedisClient()


async def get_redis() -> redis.Redis:
    return await redis_client.get_client()
