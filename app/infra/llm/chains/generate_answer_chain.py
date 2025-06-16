"""RAG chain for generating answers from document context."""

from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.fallbacks import RunnableWithFallbacks
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from app.infra.llm.prompts import RAG_PROMPT


class RAGChain:
    """Chain responsible for generating answers using retrieved document context."""

    def __init__(self):
        """Initialize the RAG chain with language model and prompt template."""
        self.llm = self._init_llm_model()
        self.prompt = self._create_prompt_template()

    def _init_llm_model(self) -> RunnableWithFallbacks:
        llm = ChatOpenAI(model="gpt-4.1-mini", max_retries=3, temperature=0.3)
        fallback_model = ChatGroq(
            model="llama-3.3-70b-versatile",
            max_retries=2,
            temperature=0.3,
        )

        llm_with_fallback = llm.with_fallbacks([fallback_model])

        return llm_with_fallback

    def _create_prompt_template(self) -> ChatPromptTemplate:
        """Create the prompt template for answer generation."""
        return ChatPromptTemplate.from_template(RAG_PROMPT)

    def generate_answer(self, question: str, docs_content: List[str]) -> str:
        """
        Generate an answer to the question using the provided document context.

        Args:
            question: The user's question
            docs_content: List of document content strings to use as context

        Returns:
            Generated answer as a string
        """
        messages = self.prompt.invoke(
            {"question": question, "context": "\n".join(docs_content)}
        )
        response = self.llm.invoke(messages)
        return response.content
