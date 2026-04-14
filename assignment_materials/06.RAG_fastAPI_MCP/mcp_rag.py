import json

from mcp.server.fastmcp import FastMCP

from app.core.rag_engine import search_documents
from app.modules.upload.service import process_pdf_from_url

mcp = FastMCP("RAG Engine")


@mcp.tool()
def upload_pdf_from_url(
    url: str,
    chunk_size: int = 500,
    overlap: int = 50,
    collection_name: str = "documents",
) -> str:
    """Download PDF from URL, extract text via OCR, chunk it, extract metadata with LLM,
    and store into ChromaDB for later search.

    Args:
        url: URL of the PDF file to process
        chunk_size: Target chunk size in tokens (default: 500)
        overlap: Overlap size between chunks (default: 50)
        collection_name: ChromaDB collection name (default: "documents")

    Returns:
        JSON string with processing results
    """
    result = process_pdf_from_url(
        url=url,
        chunk_size=chunk_size,
        overlap=overlap,
        collection_name=collection_name,
    )
    return json.dumps(result, indent=2)


@mcp.tool()
def search_rag_documents(
    query: str,
    top_k: int = 5,
    collection_name: str = "documents",
) -> str:
    """Search for relevant documents in ChromaDB using hybrid search.
    Combines embedding similarity with keyword/topic metadata boosting.

    Args:
        query: Search query text
        top_k: Number of results to return (default: 5)
        collection_name: ChromaDB collection name (default: "documents")

    Returns:
        JSON string with search results
    """
    results = search_documents(
        query=query,
        collection_name=collection_name,
        top_k=top_k,
    )
    return json.dumps(results, indent=2)


@mcp.tool()
def list_documents(
    collection_name: str = "documents",
    limit: int = 100,
) -> str:
    """List all document chunks stored in ChromaDB.

    Args:
        collection_name: ChromaDB collection name (default: "documents")
        limit: Maximum number of documents to return (default: 100)

    Returns:
        JSON string with list of documents
    """
    import chromadb

    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name=collection_name)
    results = collection.get(limit=limit, include=["documents", "metadatas"])

    documents = []
    for i, doc_id in enumerate(results["ids"]):
        meta = results["metadatas"][i]
        documents.append(
            {
                "id": doc_id,
                "text": results["documents"][i],
                "metadata": {
                    "source_file": meta.get("source_file", ""),
                    "chunk_index": meta.get("chunk_index", 0),
                    "keywords": json.loads(meta.get("keywords", "[]")),
                    "topics": json.loads(meta.get("topics", "[]")),
                },
            }
        )

    return json.dumps({"total": len(documents), "documents": documents}, indent=2)


@mcp.tool()
def get_document(
    document_id: str,
    collection_name: str = "documents",
) -> str:
    """Get a specific document chunk by its ID from ChromaDB.

    Args:
        document_id: The document ID (e.g., "document.pdf_0")
        collection_name: ChromaDB collection name (default: "documents")

    Returns:
        JSON string with document details
    """
    import chromadb

    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name=collection_name)
    results = collection.get(ids=[document_id], include=["documents", "metadatas"])

    if not results["ids"]:
        return json.dumps({"error": "Document not found"})

    meta = results["metadatas"][0]
    return json.dumps(
        {
            "id": results["ids"][0],
            "text": results["documents"][0],
            "metadata": {
                "source_file": meta.get("source_file", ""),
                "source_path": meta.get("source_path", ""),
                "chunk_index": meta.get("chunk_index", 0),
                "chunk_position": meta.get("chunk_position", 0.0),
                "token_count": meta.get("token_count", 0),
                "keywords": json.loads(meta.get("keywords", "[]")),
                "topics": json.loads(meta.get("topics", "[]")),
                "language": meta.get("language", "unknown"),
            },
        },
        indent=2,
    )


if __name__ == "__main__":
    mcp.run()
