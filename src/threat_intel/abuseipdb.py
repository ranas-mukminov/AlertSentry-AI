import aiohttp
from typing import Dict, Any, Optional
from src.config import get_config
from src.utils.logging import get_logger
from .cache import ti_cache

logger = get_logger(__name__)

class AbuseIPDBClient:
    def __init__(self):
        self.config = get_config().threat_intel.abuseipdb
        self.base_url = "https://api.abuseipdb.com/api/v2"
        self.headers = {
            "Key": self.config.get("api_key", ""),
            "Accept": "application/json"
        }

    async def check_ip(self, ip: str) -> Optional[Dict[str, Any]]:
        if not self.config.get("enabled"):
            return None

        # Check cache
        cached = await ti_cache.get(f"abuse:ip:{ip}")
        if cached:
            return cached

        try:
            params = {
                "ipAddress": ip,
                "maxAgeInDays": 90
            }
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(f"{self.base_url}/check", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        result = data.get("data", {})
                        
                        # Cache result
                        await ti_cache.set(f"abuse:ip:{ip}", result)
                        return result
                    else:
                        logger.error(f"AbuseIPDB API error: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error querying AbuseIPDB: {e}")
            return None
