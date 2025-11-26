import aiohttp
from datetime import datetime
from typing import AsyncGenerator, Dict, Any
from src.models.alert import UnifiedAlert, Severity
from src.config import get_config
from .base import BaseIngestor
from src.utils.logging import get_logger

logger = get_logger(__name__)

class ElasticIngestor(BaseIngestor):
    def __init__(self):
        super().__init__("elastic")
        self.config = get_config().sources.elastic

    async def fetch_alerts(self) -> AsyncGenerator[UnifiedAlert, None]:
        if not self.config.enabled:
            return

        try:
            # Mock implementation
            logger.info("Polling Elastic for new alerts...")
            
            mock_alert = {
                "_id": "elastic-456",
                "_source": {
                    "@timestamp": datetime.utcnow().isoformat(),
                    "signal": {
                        "rule": {
                            "severity": "medium",
                            "name": "Process Injection Detected"
                        },
                        "reason": "Suspicious process injection into lsass.exe"
                    },
                    "process": {
                        "name": "mimikatz.exe"
                    },
                    "host": {
                        "name": "win-server-01"
                    }
                }
            }
            
            yield await self.normalize_alert(mock_alert)

        except Exception as e:
            logger.error(f"Error fetching alerts from Elastic: {e}")

    async def test_connection(self) -> bool:
        if not self.config.enabled:
            return False
        return True

    async def normalize_alert(self, raw_alert: Dict[str, Any]) -> UnifiedAlert:
        source = raw_alert.get("_source", {})
        signal = source.get("signal", {})
        
        return UnifiedAlert(
            id=raw_alert.get("_id"),
            source=self.source_name,
            timestamp=datetime.fromisoformat(source.get("@timestamp")),
            severity=Severity[signal.get("rule", {}).get("severity", "INFO").upper()],
            title=signal.get("rule", {}).get("name", "Unknown Alert"),
            description=signal.get("reason", ""),
            process=source.get("process", {}).get("name"),
            hostname=source.get("host", {}).get("name"),
            metadata={"raw": raw_alert}
        )
