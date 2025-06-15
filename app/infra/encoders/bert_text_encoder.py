from collections import Counter
from typing import Any, Dict, List

from transformers import BertTokenizerFast

from app.domain.interfaces.text_encoder_interface import TextEncoder


class BertTextEncoder(TextEncoder):
    """BERT-based sparse text encoder."""

    def __init__(self, model_name: str = "bert-base-multilingual-uncased"):
        """
        Initialize BERT text encoder.

        Args:
            model_name: BERT model name for tokenization
        """
        self.model_name = model_name
        self.tokenizer = BertTokenizerFast.from_pretrained(model_name)

    def _tokenize_to_sparse_vector(self, text: str) -> Dict[str, List]:
        """Convert text to sparse vector representation."""
        inputs = self.tokenizer(text, padding=True, truncation=True, max_length=512)[
            "input_ids"
        ]

        # Convert to frequency dictionary
        token_freq = dict(Counter(inputs))

        # Filter special tokens and create indices/values
        indices = []
        values = []
        for idx, freq in token_freq.items():
            if idx not in [101, 102, 103, 0]:  # Filter BERT special tokens
                indices.append(idx)
                values.append(float(freq))

        return {"indices": indices, "values": values}

    async def encode_texts(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Encode texts using BERT tokenization to sparse vectors."""
        encoded_texts = []

        for text in texts:
            sparse_vector = self._tokenize_to_sparse_vector(text)
            encoded_texts.append(
                {
                    "text": text,
                    "vector": sparse_vector,
                    "dimension": len(sparse_vector["indices"]),
                }
            )

        return encoded_texts
