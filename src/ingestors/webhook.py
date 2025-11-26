from datetime import datetime
from typing import AsyncGenerator, Dict, Any
from src.models.alert import UnifiedAlert, Severity
from .base import BaseIngestor
from src.utils.logging import get_logger

logger = get_logger(__name__)

class WebhookIngestor(BaseIngestor):
    def __init__(self):
        super().__init__("webhook")

    async def fetch_alerts(self) -> AsyncGenerator[UnifiedAlert, None]:
        # Webhook is push-based, so this might be unused or used to process queued webhooks
        pass

    async def test_connection(self) -> bool:
        return True

    async def process_webhook(self, payload: Dict[str, Any]) -> UnifiedAlert:
        """
        Process an incoming webhook payload
        """
        return await self.normalize_alert(payload)

    async def normalize_alert(self, raw_alert: Dict[str, Any]) -> UnifiedAlert:
        # Assumes the webhook payload matches our schema or is close to it
        # In a real app, we might need different normalizers for different webhook sources
        return UnifiedAlert(
            id=raw_alert.get("id", f"webhook-{datetime.utcnow().timestamp()}"),
            source=self.source_name,
            timestamp=datetime.fromisoformat(raw_alert.get("timestamp", datetime.utcnow().isoformat())),
            severity=Severity[raw_alert.get("severity", "INFO").upper()],
            title=raw_alert.get("title", "Webhook Alert"),
            description=raw_alert.get("description", ""),
            source_ip=raw_alert.get("source_ip"),
            destination_ip=raw_alert.get("destination_ip"),
            user=raw_alert.get("user"),
            hostname=raw_alert.get("hostname"),
            metadata={"raw": raw_alert}
        )
