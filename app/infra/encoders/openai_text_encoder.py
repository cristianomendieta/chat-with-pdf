from typing import Any, Dict, List

from langchain_openai import OpenAIEmbeddings

from app.domain.interfaces.text_encoder_interface import TextEncoder


class OpenAITextEncoder(TextEncoder):
    """OpenAI-based dense text encoder."""

    def __init__(self, model_name: str = "text-embedding-3-small"):
        """
        Initialize OpenAI text encoder.

        Args:
            model_name: OpenAI embedding model name
        """
        self.model_name = model_name
        self.embeddings = OpenAIEmbeddings(model=model_name)
        self._dimension = 1536

    async def encode_texts(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Encode texts using OpenAI embeddings."""
        vectors = self.embeddings.embed_documents(texts)

        encoded_texts = []
        for text, vector in zip(texts, vectors):
            encoded_texts.append(
                {
                    "text": text,
                    "vector": vector,
                    "dimension": len(vector),
                }
            )

        return encoded_texts

    def get_encoding_type(self) -> str:
        return "dense"
