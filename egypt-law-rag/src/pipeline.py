"""
End-to-end ingestion pipeline orchestration.

Flow: PDF -> extract -> clean -> chunk -> embed -> Qdrant
"""

from pathlib import Path

from src.config import CHUNKS_PATH, PDF_PATH
from src.data.chunk_and_metadata import chunk_documents
from src.data.clean import clean_text
from src.data.extract import extract_pdf
from src.vector_store import build_index


def run_ingest(pdf_path: Path | str | None = None, law_name: str = "قانون العقوبات المصري") -> dict:
    """
    Run the full document ingestion pipeline on a PDF.

    Steps: extract -> clean -> chunk
    """
    pdf = Path(pdf_path) if pdf_path else PDF_PATH
    steps = []

    print("Step 1/3: Extracting text from PDF...")
    extract_pdf(pdf_path=pdf)
    steps.append("extract")

    print("Step 2/3: Cleaning Arabic text...")
    clean_text()
    steps.append("clean")

    print("Step 3/3: Chunking articles with metadata...")
    chunks = chunk_documents(law_name=law_name)
    steps.append("chunk")

    return {
        "status": "completed",
        "pdf": str(pdf),
        "chunks_path": str(CHUNKS_PATH),
        "chunk_count": len(chunks),
        "steps": steps,
    }


def run_index() -> dict:
    """Embed chunks and store in Qdrant."""
    print("Indexing chunks into vector database...")
    count = build_index()
    return {"status": "completed", "indexed_count": count}


def run_full_pipeline(pdf_path: Path | str | None = None, law_name: str = "قانون العقوبات المصري") -> dict:
    """Run ingest + index — full path from PDF to queryable vector store."""
    ingest_result = run_ingest(pdf_path=pdf_path, law_name=law_name)
    index_result = run_index()
    return {
        "status": "completed",
        "ingest": ingest_result,
        "index": index_result,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Egypt Law RAG pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("ingest", help="PDF -> extract -> clean -> chunk")
    sub.add_parser("index", help="Embed chunks and store in Qdrant")
    sub.add_parser("full", help="Run ingest + index")

    ingest_parser = sub.add_parser("ingest-pdf", help="Ingest a specific PDF file")
    ingest_parser.add_argument("pdf", type=str, help="Path to PDF file")

    full_parser = sub.add_parser("full-pdf", help="Full pipeline for a specific PDF")
    full_parser.add_argument("pdf", type=str, help="Path to PDF file")

    args = parser.parse_args()

    if args.command == "ingest":
        print(run_ingest())
    elif args.command == "index":
        print(run_index())
    elif args.command == "full":
        print(run_full_pipeline())
    elif args.command == "ingest-pdf":
        print(run_ingest(pdf_path=args.pdf))
    elif args.command == "full-pdf":
        print(run_full_pipeline(pdf_path=args.pdf))
