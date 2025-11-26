from abc import ABC, abstractmethod
from typing import List, AsyncGenerator
from src.models.alert import UnifiedAlert
from src.utils.logging import get_logger

logger = get_logger(__name__)

class BaseIngestor(ABC):
    def __init__(self, source_name: str):
        self.source_name = source_name

    @abstractmethod
    async def fetch_alerts(self) -> AsyncGenerator[UnifiedAlert, None]:
        """
        Poll for new alerts from the source
        """
        pass

    @abstractmethod
    async def test_connection(self) -> bool:
        """
        Verify connectivity to the source
        """
        pass

    async def normalize_alert(self, raw_alert: dict) -> UnifiedAlert:
        """
        Convert raw alert to UnifiedAlert
        """
        raise NotImplementedError
