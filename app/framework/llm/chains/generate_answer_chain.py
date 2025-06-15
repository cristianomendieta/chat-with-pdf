from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from typing_extensions import List

from app.framework.llm.prompts.rag_generate_answer import RAG_PROMPT


class RAGChain:
    def __init__(self):
        self.llm = init_chat_model("gpt-4o-mini")
        self.prompt = self._create_prompt_template()

    def _create_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_template(RAG_PROMPT)

    def generate_answer(self, question: str, docs_content: List[Document]) -> dict:
        messages = self.prompt.invoke({"question": question, "context": docs_content})
        response = self.llm.invoke(messages)
        return {"answer": response.content}
