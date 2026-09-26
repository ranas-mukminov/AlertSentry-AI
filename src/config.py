import os
import yaml
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class LLMConfig(BaseModel):
    provider: str
    model: str
    api_key: str
    temperature: float = 0.1
    max_tokens: int = 2000
    timeout: int = 30
    retry_attempts: int = 3


class SplunkConfig(BaseModel):
    enabled: bool = False
    url: Optional[str] = None
    token: Optional[str] = None
    saved_search: Optional[str] = None
    poll_interval: int = 60


class ElasticConfig(BaseModel):
    enabled: bool = False
    url: Optional[str] = None
    api_key: Optional[str] = None
    index: Optional[str] = None
    poll_interval: int = 30


class SourcesConfig(BaseModel):
    splunk: SplunkConfig = Field(default_factory=SplunkConfig)
    elastic: ElasticConfig = Field(default_factory=ElasticConfig)


class ThreatIntelConfig(BaseModel):
    virustotal: Dict[str, Any] = Field(default_factory=dict)
    abuseipdb: Dict[str, Any] = Field(default_factory=dict)


class OutputsConfig(BaseModel):
    slack: Dict[str, Any] = Field(default_factory=dict)
    jira: Dict[str, Any] = Field(default_factory=dict)


class DatabaseConfig(BaseModel):
    postgres: Dict[str, Any]
    redis: Dict[str, Any]


class AnalysisConfig(BaseModel):
    batch_size: int = 10
    batch_timeout: int = 5
    confidence_threshold: int = 70
    auto_close_fp: bool = True
    include_historical_context: bool = True
    historical_lookback_hours: int = 24


class AppConfig(BaseSettings):
    llm: LLMConfig
    sources: SourcesConfig
    threat_intel: ThreatIntelConfig
    outputs: OutputsConfig
    database: DatabaseConfig
    analysis: AnalysisConfig

    @classmethod
    def load(cls, config_path: str = "config/config.yaml") -> "AppConfig":
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "r") as f:
            raw_config = yaml.safe_load(f)

        # Expand environment variables in the config
        expanded_config = cls._expand_env_vars(raw_config)

        return cls(**expanded_config.get("alertsentry", {}))

    @staticmethod
    def _expand_env_vars(config: Any) -> Any:
        if isinstance(config, dict):
            return {k: AppConfig._expand_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [AppConfig._expand_env_vars(v) for v in config]
        elif isinstance(config, str):
            if config.startswith("${") and config.endswith("}"):
                env_var = config[2:-1]
                return os.getenv(env_var, config)
            return config
        else:
            return config


# Global config instance
settings: Optional[AppConfig] = None


def load_config(path: str = "config/config.yaml") -> AppConfig:
    global settings
    settings = AppConfig.load(path)
    return settings


def get_config() -> AppConfig:
    if settings is None:
        return load_config()
    return settings
