"""Environment configuration and settings management."""

from functools import lru_cache
from os import environ


class EnvironmentSettings:
    """Environment configuration settings for the application."""

    PINECONE_API_KEY = environ.get("PINECONE_API_KEY")
    PINECONE_DENSE_INDEX_NAME = environ.get(
        "PINECONE_DENSE_INDEX_NAME", "dense-chat-with-pdf"
    )
    PINECONE_SPARSE_INDEX_NAME = environ.get(
        "PINECONE_SPARSE_INDEX_NAME", "sparse-chat-with-pdf"
    )


@lru_cache
def get_env() -> EnvironmentSettings:
    """
    Get cached environment settings instance.

    Returns:
        Singleton instance of environment settings
    """
    return EnvironmentSettings()
