from typing import Any, Dict, List, Tuple

from langchain.schema import Document
from langchain_core.messages import HumanMessage, SystemMessage

from backend.config import get_settings
from backend.prompts.research_prompt import SYSTEM_INSTRUCTIONS, research_prompt
from backend.rag.retriever import RAGRetriever
from backend.services.openai_client import get_chat_client

settings = get_settings()


class RAGPipeline:
    """
    End-to-end RAG pipeline: retrieve context, construct prompt,
    call LLM, and return answer + sources.
    """

    def __init__(self, retriever: RAGRetriever | None = None):
        self.retriever = retriever or RAGRetriever()
        self.chat_client = get_chat_client(temperature=0.0)

    @staticmethod
    def _format_context_with_sources(chunks: List[Document]) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Format retrieved chunks into a context string with explicit source labels,
        and return structured source info for the API response.
        """
        context_parts: List[str] = []
        sources: List[Dict[str, Any]] = []

        for idx, doc in enumerate(chunks, start=1):
            label = f"Source {idx}"
            text = doc.page_content
            source_meta = doc.metadata or {}
            source_info = {
                "label": label,
                "text": text,
                "metadata": source_meta,
            }
            sources.append(source_info)

            context_parts.append(f"{label}:\n{text}\n")

        context_str = "\n---\n".join(context_parts) if context_parts else ""
        return context_str, sources

    def answer_question(self, question: str) -> Dict[str, Any]:
        """
        Main entry: given a user question, run retrieval + generation
        and return an answer and sources.
        """
        chunks = self.retriever.retrieve(question)

        if not chunks:
            return {
                "answer": "I could not find information in the documents.",
                "sources": [],
            }

        context_str, sources = self._format_context_with_sources(chunks)

        prompt_text = research_prompt.format(
            context=context_str,
            question=question,
            system_instructions=SYSTEM_INSTRUCTIONS.strip(),
        )

        messages = [
            SystemMessage(content=SYSTEM_INSTRUCTIONS.strip()),
            HumanMessage(content=prompt_text),
        ]

        response = self.chat_client.invoke(messages)
        answer = response.content if hasattr(response, "content") else str(response)

        normalized = answer.strip().lower()
        if not normalized or "i could not find information in the documents" in normalized:
            safe_answer = "I could not find information in the documents."
            return {
                "answer": safe_answer,
                "sources": [],
            }

        return {
            "answer": answer,
            "sources": sources,
        }

