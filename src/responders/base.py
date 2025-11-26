from abc import ABC, abstractmethod
from src.models.analysis import AnalysisResult
from src.utils.logging import get_logger

logger = get_logger(__name__)

class BaseResponder(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def handle_analysis(self, analysis: AnalysisResult) -> bool:
        """
        Take action based on analysis result
        """
        pass
