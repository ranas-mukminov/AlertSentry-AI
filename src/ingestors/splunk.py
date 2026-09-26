import aiohttp
from datetime import datetime
from typing import AsyncGenerator, Dict, Any
from src.models.alert import UnifiedAlert, Severity
from src.config import get_config
from .base import BaseIngestor
from src.utils.logging import get_logger

logger = get_logger(__name__)


class SplunkIngestor(BaseIngestor):
    def __init__(self):
        super().__init__("splunk")
        self.config = get_config().sources.splunk

    async def fetch_alerts(self) -> AsyncGenerator[UnifiedAlert, None]:
        if not self.config.enabled:
            return

        try:
            async with aiohttp.ClientSession():
                # Mock implementation for now as we don't have a real Splunk instance
                # In a real scenario, we would call the Splunk REST API
                # url = f"{self.config.url}/services/search/jobs/export"

                # Simulating fetching alerts
                logger.info("Polling Splunk for new alerts...")

                # Yield a mock alert for demonstration
                mock_alert = {
                    "id": "splunk-123",
                    "timestamp": datetime.utcnow().isoformat(),
                    "severity": "high",
                    "title": "Suspicious Login Attempt",
                    "description": "Multiple failed login attempts detected from IP 192.168.1.100",
                    "source_ip": "192.168.1.100",
                    "user": "admin",
                }

                yield await self.normalize_alert(mock_alert)

        except Exception as e:
            logger.error(f"Error fetching alerts from Splunk: {e}")

    async def test_connection(self) -> bool:
        if not self.config.enabled:
            return False
        # Mock connection test
        return True

    async def normalize_alert(self, raw_alert: Dict[str, Any]) -> UnifiedAlert:
        return UnifiedAlert(
            id=raw_alert.get("id"),
            source=self.source_name,
            timestamp=datetime.fromisoformat(raw_alert.get("timestamp")),
            severity=Severity[raw_alert.get("severity").upper()],
            title=raw_alert.get("title"),
            description=raw_alert.get("description"),
            source_ip=raw_alert.get("source_ip"),
            user=raw_alert.get("user"),
            metadata={"raw": raw_alert},
        )
