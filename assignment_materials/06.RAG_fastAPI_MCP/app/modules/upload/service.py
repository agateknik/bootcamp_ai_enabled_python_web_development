import tempfile
from pathlib import Path

import httpx

from app.core.rag_engine import (
    chunk_text_recursive,
    extract_chunk_metadata_with_llm,
    extract_ocr_from_pdf,
    insert_chunks_to_chromadb,
)


def download_pdf_from_url(url: str) -> str:
    """Download PDF from URL and save to temporary file.

    Args:
        url: URL to the PDF file

    Returns:
        Path to the downloaded temporary PDF file
    """
    response = httpx.get(url, follow_redirects=True, timeout=30.0)
    response.raise_for_status()

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_file.write(response.content)
    temp_file.close()

    return temp_file.name


def process_pdf_from_url(
    url: str,
    chunk_size: int = 500,
    overlap: int = 50,
    collection_name: str = "documents",
    persist_directory: str = "./chroma_db",
) -> dict:
    """Download and process PDF from URL through full RAG pipeline.

    Args:
        url: URL to the PDF file
        chunk_size: Target chunk size in tokens (default: 500)
        overlap: Overlap size between chunks (default: 50)
        collection_name: ChromaDB collection name
        persist_directory: ChromaDB persist directory

    Returns:
        Dictionary with processing results
    """
    temp_path = download_pdf_from_url(url)

    try:
        # Step 1: Extract OCR
        extracted_text = extract_ocr_from_pdf(temp_path)

        # Step 2: Chunk text
        chunks = chunk_text_recursive(
            extracted_text, chunk_size=chunk_size, overlap=overlap
        )

        # Step 3: Extract metadata for each chunk
        enriched_chunks = []
        for chunk in chunks:
            llm_metadata = extract_chunk_metadata_with_llm(chunk["text"])
            pdf_file = Path(temp_path)
            stat = pdf_file.stat()

            enriched_chunks.append(
                {
                    **chunk,
                    "metadata": {
                        "source_file": pdf_file.name,
                        "source_path": str(pdf_file.absolute()),
                        "file_size_bytes": stat.st_size,
                        "total_chunks": len(chunks),
                        "chunk_index": chunk["start_index"],
                        "chunk_position": round(
                            (chunk["start_index"] + 1) / len(chunks) * 100, 1
                        ),
                        **llm_metadata,
                    },
                }
            )

        # Step 4: Insert to ChromaDB
        chromadb_result = insert_chunks_to_chromadb(
            enriched_chunks,
            collection_name=collection_name,
            persist_directory=persist_directory,
        )

        return {
            "source_url": url,
            "source_file": pdf_file.name,
            "total_pages_text_length": len(extracted_text),
            "total_chunks": len(chunks),
            "chromadb_result": chromadb_result,
        }
    finally:
        Path(temp_path).unlink(missing_ok=True)
