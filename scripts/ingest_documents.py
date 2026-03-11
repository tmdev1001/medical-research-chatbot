import argparse

from backend.rag.ingest import ingest_documents


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest clinical documents and build FAISS index."
    )
    parser.add_argument(
        "--documents-path",
        type=str,
        default=None,
        help="Path to folder containing PDF/TXT documents (overrides config).",
    )
    parser.add_argument(
        "--index-path",
        type=str,
        default=None,
        help="Path where FAISS index will be stored (overrides config).",
    )
    args = parser.parse_args()

    ingest_documents(
        documents_path=args.documents_path,
        faiss_index_path=args.index_path,
    )


if __name__ == "__main__":
    main()

