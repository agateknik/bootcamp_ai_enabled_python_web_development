import json

import chromadb
from fastapi import APIRouter, HTTPException

from app.modules.documents.schema import (
    DocumentDetailResponse,
    DocumentListResponse,
)

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    collection_name: str = "documents",
    persist_directory: str = "./chroma_db",
    limit: int = 100,
):
    """List all documents in ChromaDB."""
    try:
        client = chromadb.PersistentClient(path=persist_directory)
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

        return DocumentListResponse(
            total=len(documents),
            documents=documents,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{document_id}", response_model=DocumentDetailResponse)
async def get_document(
    document_id: str,
    collection_name: str = "documents",
    persist_directory: str = "./chroma_db",
):
    """Get document detail by ID."""
    try:
        client = chromadb.PersistentClient(path=persist_directory)
        collection = client.get_collection(name=collection_name)

        results = collection.get(ids=[document_id], include=["documents", "metadatas"])

        if not results["ids"]:
            raise HTTPException(status_code=404, detail="Document not found")

        meta = results["metadatas"][0]
        return DocumentDetailResponse(
            id=results["ids"][0],
            text=results["documents"][0],
            metadata={
                "source_file": meta.get("source_file", ""),
                "source_path": meta.get("source_path", ""),
                "chunk_index": meta.get("chunk_index", 0),
                "chunk_position": meta.get("chunk_position", 0.0),
                "token_count": meta.get("token_count", 0),
                "keywords": json.loads(meta.get("keywords", "[]")),
                "topics": json.loads(meta.get("topics", "[]")),
                "language": meta.get("language", "unknown"),
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
