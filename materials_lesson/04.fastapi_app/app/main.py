from fastapi import FastAPI

from scalar_fastapi import get_scalar_api_reference

from app.router.books_router import books_router


app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(books_router)


@app.get("/scalar")
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url)
