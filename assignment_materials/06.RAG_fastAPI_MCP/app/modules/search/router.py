from fastapi import APIRouter, HTTPException, Query

from app.core.rag_engine import search_documents
from app.modules.search.schema import SearchResponse

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("", response_model=SearchResponse)
async def search(
    q: str = Query(..., description="Search query text"),
    top_k: int = Query(default=5, description="Number of results to return"),
    collection_name: str = Query(
        default="documents", description="ChromaDB collection name"
    ),
    persist_directory: str = Query(
        default="./chroma_db", description="ChromaDB persist directory"
    ),
):
    """Search for relevant documents using hybrid search with metadata boosting."""
    try:
        results = search_documents(
            query=q,
            collection_name=collection_name,
            persist_directory=persist_directory,
            top_k=top_k,
        )

        return SearchResponse(
            query=q,
            total_results=len(results),
            results=results,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
