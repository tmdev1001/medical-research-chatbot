import os
from typing import List

from langchain.schema import Document
from langchain_community.vectorstores import FAISS

from backend.config import get_settings
from backend.services.openai_client import get_embedding_client

settings = get_settings()


class RAGRetriever:
    """
    Wrapper around FAISS vector store for retrieving relevant chunks.
    """

    def __init__(self, index_path: str | None = None, top_k: int | None = None):
        self.index_path = index_path or settings.faiss_index_path
        self.top_k = top_k or settings.top_k
        self._vector_store: FAISS | None = None
        self._load_index()

    def _load_index(self) -> None:
        if not os.path.isdir(self.index_path):
            raise FileNotFoundError(
                f"FAISS index not found at '{self.index_path}'. "
                "Run the ingest script first: `python scripts/ingest_documents.py`."
            )
        embeddings = get_embedding_client()
        self._vector_store = FAISS.load_local(
            self.index_path,
            embeddings,
            allow_dangerous_deserialization=True,
        )

    def retrieve(self, query: str) -> List[Document]:
        if self._vector_store is None:
            self._load_index()
        assert self._vector_store is not None
        docs = self._vector_store.similarity_search(query, k=self.top_k)
        return docs

