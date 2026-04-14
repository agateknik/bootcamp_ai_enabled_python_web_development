from fastapi import APIRouter, HTTPException

from app.modules.upload.schema import UploadFromUrlRequest, UploadResponse
from app.modules.upload.service import process_pdf_from_url

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("", response_model=UploadResponse)
async def upload_from_url(request: UploadFromUrlRequest):
    """Upload and process PDF from URL."""
    try:
        result = process_pdf_from_url(
            url=str(request.url),
            chunk_size=request.chunk_size,
            overlap=request.overlap,
            collection_name=request.collection_name,
        )

        return UploadResponse(
            success=True,
            message="PDF processed successfully",
            source_file=result["source_file"],
            source_url=result.get("source_url"),
            total_chunks=result["total_chunks"],
            total_text_length=result["total_pages_text_length"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
