import json
from datetime import datetime
from typing import Optional
from src.models.alert import UnifiedAlert
from src.models.analysis import AnalysisResult, Classification, Severity
from src.analyzers.llm_client import LLMClient
from src.analyzers.context_builder import ContextBuilder
from src.analyzers.prompts import TRIAGE_PROMPT
from src.utils.logging import get_logger

logger = get_logger(__name__)

class AlertClassifier:
    def __init__(self):
        self.llm = LLMClient()
        self.context_builder = ContextBuilder()

    async def analyze(self, alert: UnifiedAlert) -> Optional[AnalysisResult]:
        logger.info(f"Starting analysis for alert {alert.id}")
        start_time = datetime.utcnow()

        # 1. Build Context
        context = await self.context_builder.build_context(alert)
        
        # 2. Prepare Prompt
        prompt = TRIAGE_PROMPT.format(
            alert_json=alert.model_dump_json(),
            threat_intel_context=json.dumps(context.get("threat_intel", {}), indent=2),
            historical_context=json.dumps(context.get("historical", []), indent=2)
        )

        # 3. Call LLM
        llm_response = await self.llm.analyze_alert(prompt)
        
        if not llm_response:
            logger.error(f"Failed to get analysis for alert {alert.id}")
            return None

        # 4. Parse Result
        end_time = datetime.utcnow()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)

        try:
            return AnalysisResult(
                alert_id=alert.id,
                classification=Classification(llm_response.get("classification", "unknown")),
                confidence=llm_response.get("confidence", 0),
                severity_adjusted=Severity(llm_response.get("severity_adjusted", alert.severity).upper()),
                reasoning=llm_response.get("reasoning", ""),
                mitre_techniques=llm_response.get("mitre_techniques", []),
                recommended_actions=llm_response.get("recommended_actions", []),
                similar_incidents=llm_response.get("similar_incidents", []),
                llm_provider=self.llm.provider,
                llm_model=self.llm.model,
                analysis_time_ms=duration_ms
            )
        except Exception as e:
            logger.error(f"Error parsing analysis result: {e}")
            return None
