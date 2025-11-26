from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from .enums import Severity

class IOC(BaseModel):
    type: str  # ip, domain, hash, url
    value: str
    reputation: Optional[Dict[str, Any]] = None

class UnifiedAlert(BaseModel):
    id: str = Field(..., description="Unique alert ID")
    source: str = Field(..., description="SIEM source name")
    source_alert_id: Optional[str] = Field(None, description="Original ID from source")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    severity: Severity
    title: str
    description: str
    raw_log: Optional[str] = None
    
    # Entities
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    user: Optional[str] = None
    hostname: Optional[str] = None
    process: Optional[str] = None
    file_hash: Optional[str] = None
    
    # Context
    mitre_tactics: List[str] = Field(default_factory=list)
    mitre_techniques: List[str] = Field(default_factory=list)
    iocs: List[IOC] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
