from scalar_fastapi import get_scalar_api_reference
from fastapi import FastAPI
from app.core.settings import settings
from app.router.tasks import task_router
from app.router.users import user_router

app = FastAPI(
    docs_url = None, 
    redoc_url = None,
    title= settings.APP_NAME,
    version = settings.VERSION
)

app.include_router(task_router, prefix="/api")
app.include_router(user_router, prefix="/api")

@app.get("/")
def get_root():
    return ({"message":f"Welcome to the {app.title} API", "version": app.version})

@app.get("/scalar")
def get_scalar():
    return get_scalar_api_reference(
        openapi_url= app.openapi_url,
        title= app.title
    )