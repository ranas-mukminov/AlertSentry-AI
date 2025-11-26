import json
from typing import Dict, Any, Optional
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
from src.config import get_config
from src.models.enums import LLMProvider
from src.utils.logging import get_logger

logger = get_logger(__name__)

class LLMClient:
    def __init__(self):
        self.config = get_config().llm
        self.provider = self.config.provider
        self.model = self.config.model
        self.api_key = self.config.api_key
        
        self.anthropic_client = None
        self.openai_client = None

        if self.provider == LLMProvider.ANTHROPIC:
            self.anthropic_client = AsyncAnthropic(api_key=self.api_key)
        elif self.provider == LLMProvider.OPENAI:
            self.openai_client = AsyncOpenAI(api_key=self.api_key)
        # Add other providers as needed

    async def analyze_alert(self, prompt: str) -> Optional[Dict[str, Any]]:
        try:
            if self.provider == LLMProvider.ANTHROPIC:
                return await self._analyze_anthropic(prompt)
            elif self.provider == LLMProvider.OPENAI:
                return await self._analyze_openai(prompt)
            else:
                logger.error(f"Unsupported LLM provider: {self.provider}")
                return None
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            return None

    async def _analyze_anthropic(self, prompt: str) -> Dict[str, Any]:
        response = await self.anthropic_client.messages.create(
            model=self.model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        content = response.content[0].text
        return self._parse_json(content)

    async def _analyze_openai(self, prompt: str) -> Dict[str, Any]:
        response = await self.openai_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return self._parse_json(content)

    def _parse_json(self, content: str) -> Dict[str, Any]:
        try:
            # Try to find JSON block if wrapped in markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            return json.loads(content.strip())
        except json.JSONDecodeError:
            logger.error(f"Failed to parse LLM response as JSON: {content}")
            raise
