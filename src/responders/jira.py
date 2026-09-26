from src.models.analysis import AnalysisResult
from src.config import get_config
from src.utils.logging import get_logger
from .base import BaseResponder

logger = get_logger(__name__)


class JiraResponder(BaseResponder):
    def __init__(self):
        super().__init__("jira")
        self.config = get_config().outputs.jira

    async def handle_analysis(self, analysis: AnalysisResult) -> bool:
        if not self.config.get("enabled"):
            return False

        create_on = self.config.get("create_on", [])
        if analysis.classification.value not in create_on:
            return False

        # Mock implementation for Jira creation
        # In a real scenario, we would use the Jira REST API
        logger.info(f"Creating Jira ticket for alert {analysis.alert_id}")
        return True
