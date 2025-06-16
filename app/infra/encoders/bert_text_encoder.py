"""BERT-based sparse text encoder implementation."""

from collections import Counter
from typing import Any, Dict, List

from transformers import BertTokenizerFast

from app.domain.interfaces.text_encoder_interface import TextEncoder


class BertTextEncoder(TextEncoder):
    """BERT-based sparse text encoder using tokenization for sparse vectors."""

    def __init__(self, model_name: str = "bert-base-multilingual-uncased"):
        """
        Initialize BERT text encoder.

        Args:
            model_name: BERT model name for tokenization
        """
        self.model_name = model_name
        self.tokenizer = BertTokenizerFast.from_pretrained(model_name)

    def _tokenize_to_sparse_vector(self, text: str) -> Dict[str, List]:
        """
        Convert text to sparse vector representation using BERT tokenization.

        Args:
            text: Input text to tokenize

        Returns:
            Sparse vector with indices and values
        """
        inputs = self.tokenizer(text, padding=True, truncation=True, max_length=512)[
            "input_ids"
        ]

        # Create frequency distribution of tokens
        token_freq = dict(Counter(inputs))

        # Filter special tokens and create sparse representation
        indices = []
        values = []
        for idx, freq in token_freq.items():
            # Skip BERT special tokens: [CLS], [SEP], [UNK], [PAD]
            if idx not in [101, 102, 103, 0]:
                indices.append(idx)
                values.append(float(freq))

        return {"indices": indices, "values": values}

    async def encode_texts(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Encode texts using BERT tokenization to create sparse vectors.

        Args:
            texts: List of text strings to encode

        Returns:
            List of sparse vector representations with metadata
        """
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

    def get_encoding_type(self) -> str:
        """Return the encoding type identifier."""
        return "sparse"
