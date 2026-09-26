from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from .enums import Classification, Severity


class AnalysisResult(BaseModel):
    alert_id: str
    classification: Classification
    confidence: int = Field(..., ge=0, le=100)
    severity_adjusted: Optional[Severity] = None
    reasoning: str
    mitre_techniques: List[str] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)
    similar_incidents: List[str] = Field(default_factory=list)

    # Metadata
    llm_provider: str
    llm_model: str
    tokens_used: int = 0
    analysis_time_ms: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AnalystFeedback(BaseModel):
    analysis_id: str
    analyst_id: str
    correct_classification: Classification
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
