from abc import ABC, abstractmethod
from typing import Any, Dict, List


class TextEncoder(ABC):
    """Abstract interface for text encoding strategies."""

    @abstractmethod
    async def encode_texts(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Encode a list of texts into vectors.

        Args:
            texts: List of text strings to encode

        Returns:
            List of encoded vectors with metadata
        """
        pass
