import os
from typing import Optional

from langchain.schema import Document
from langchain_community.vectorstores import FAISS

from backend.config import get_settings
from backend.services.openai_client import get_embedding_client
from backend.utils.chunking import chunk_documents
from backend.utils.loader import load_documents_from_folder

settings = get_settings()


def ingest_documents(
    documents_path: Optional[str] = None,
    faiss_index_path: Optional[str] = None,
) -> None:
    """
    Load, chunk, embed, and store clinical documents in a FAISS index.
    """
    documents_dir = documents_path or settings.documents_path
    index_dir = faiss_index_path or settings.faiss_index_path

    os.makedirs(index_dir, exist_ok=True)

    print(f"Loading documents from: {documents_dir}")
    docs: list[Document] = load_documents_from_folder(documents_dir)
    print(f"Loaded {len(docs)} documents/pages.")

    print("Chunking documents...")
    chunks = chunk_documents(docs)
    print(f"Created {len(chunks)} chunks.")

    print("Creating embeddings and building FAISS index...")
    embedding_client = get_embedding_client()
    vector_store = FAISS.from_documents(chunks, embedding_client)

    print(f"Saving FAISS index to: {index_dir}")
    vector_store.save_local(index_dir)
    print("Ingestion completed successfully.")

