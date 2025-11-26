import aiohttp
from typing import Dict, Any, Optional
from src.config import get_config
from src.utils.logging import get_logger
from .cache import ti_cache

logger = get_logger(__name__)

class VirusTotalClient:
    def __init__(self):
        self.config = get_config().threat_intel.virustotal
        self.base_url = "https://www.virustotal.com/api/v3"
        self.headers = {
            "x-apikey": self.config.get("api_key", "")
        }

    async def get_ip_report(self, ip: str) -> Optional[Dict[str, Any]]:
        if not self.config.get("enabled"):
            return None

        # Check cache
        cached = await ti_cache.get(f"vt:ip:{ip}")
        if cached:
            return cached

        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(f"{self.base_url}/ip_addresses/{ip}") as response:
                    if response.status == 200:
                        data = await response.json()
                        result = data.get("data", {}).get("attributes", {})
                        
                        # Cache result
                        await ti_cache.set(f"vt:ip:{ip}", result)
                        return result
                    elif response.status == 404:
                        return None
                    else:
                        logger.error(f"VirusTotal API error: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error querying VirusTotal: {e}")
            return None

    async def get_file_report(self, file_hash: str) -> Optional[Dict[str, Any]]:
        if not self.config.get("enabled"):
            return None

        # Check cache
        cached = await ti_cache.get(f"vt:hash:{file_hash}")
        if cached:
            return cached

        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(f"{self.base_url}/files/{file_hash}") as response:
                    if response.status == 200:
                        data = await response.json()
                        result = data.get("data", {}).get("attributes", {})
                        
                        # Cache result (longer TTL for hashes)
                        await ti_cache.set(f"vt:hash:{file_hash}", result, ttl=604800) # 7 days
                        return result
                    elif response.status == 404:
                        return None
                    else:
                        logger.error(f"VirusTotal API error: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error querying VirusTotal: {e}")
            return None
