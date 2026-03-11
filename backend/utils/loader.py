import glob
import os
from typing import List

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.schema import Document


def load_documents_from_folder(folder_path: str) -> List[Document]:
    """
    Load PDF and TXT documents from a folder into LangChain Document objects.
    """
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Documents folder not found: {folder_path}")

    pattern_pdf = os.path.join(folder_path, "**", "*.pdf")
    pattern_txt = os.path.join(folder_path, "**", "*.txt")

    file_paths = glob.glob(pattern_pdf, recursive=True) + glob.glob(
        pattern_txt, recursive=True
    )

    documents: List[Document] = []

    for path in file_paths:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(path)
        elif ext == ".txt":
            loader = TextLoader(path, encoding="utf-8")
        else:
            continue

        loaded_docs = loader.load()
        for d in loaded_docs:
            d.metadata = d.metadata or {}
            d.metadata.setdefault("source", path)
        documents.extend(loaded_docs)

    if not documents:
        raise ValueError(f"No PDF or TXT documents found in {folder_path}")

    return documents

