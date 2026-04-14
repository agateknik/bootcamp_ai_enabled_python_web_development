from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.modules.documents.router import router as documents_router
from app.modules.search.router import router as search_router
from app.modules.upload.router import router as upload_router

app = FastAPI(
    title="RAG Engine API",
    description="API for RAG Engine with FastAPI and MCP",
    version="0.1.0",
)

app.include_router(upload_router)
app.include_router(documents_router)
app.include_router(search_router)


@app.get("/scalar")
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


@app.get("/")
async def root():
    return {"message": "RAG Engine API is running"}
