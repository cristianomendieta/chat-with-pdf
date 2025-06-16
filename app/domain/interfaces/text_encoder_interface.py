"""Abstract interface for text encoding operations."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class TextEncoder(ABC):
    """Abstract interface for converting text into vector representations."""

    @abstractmethod
    async def encode_texts(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Encode a list of text strings into vector representations.

        Args:
            texts: List of text strings to encode

        Returns:
            List of encoded vectors with associated metadata
        """
        pass
