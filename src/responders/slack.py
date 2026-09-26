from src.models.analysis import AnalysisResult
import aiohttp
from src.config import get_config
from src.utils.logging import get_logger
from .base import BaseResponder

logger = get_logger(__name__)


class SlackResponder(BaseResponder):
    def __init__(self):
        super().__init__("slack")
        self.config = get_config().outputs.slack

    async def handle_analysis(self, analysis: AnalysisResult) -> bool:
        if not self.config.get("enabled"):
            return False

        notify_on = self.config.get("notify_on", [])
        if analysis.classification.value not in notify_on:
            return False

        webhook_url = self.config.get("webhook_url")
        if not webhook_url:
            logger.warning("Slack enabled but no webhook URL configured")
            return False

        try:
            payload = self._build_payload(analysis)
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload) as response:
                    if response.status == 200:
                        logger.info(
                            f"Sent notification to Slack for alert {analysis.alert_id}"
                        )
                        return True
                    else:
                        logger.error(
                            f"Failed to send Slack notification: {response.status}"
                        )
                        return False
        except Exception as e:
            logger.error(f"Error sending Slack notification: {e}")
            return False

    def _build_payload(self, analysis: AnalysisResult) -> dict:
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🚨 Alert Analysis: {analysis.classification.value.upper()}",
                },
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Alert ID:*\n{analysis.alert_id}"},
                    {
                        "type": "mrkdwn",
                        "text": f"*Confidence:*\n{analysis.confidence}%",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Severity:*\n{analysis.severity_adjusted.value}",
                    },
                    {"type": "mrkdwn", "text": f"*Model:*\n{analysis.llm_model}"},
                ],
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Reasoning:*\n{analysis.reasoning}",
                },
            },
        ]

        if analysis.recommended_actions:
            actions_text = "\n".join(
                [f"• {action}" for action in analysis.recommended_actions]
            )
            blocks.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Recommended Actions:*\n{actions_text}",
                    },
                }
            )

        return {"blocks": blocks}
