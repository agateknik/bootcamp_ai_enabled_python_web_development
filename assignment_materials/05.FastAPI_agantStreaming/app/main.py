from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference

from app.modules.sessions.router import session_router
from app.modules.chats.router import chat_router

app = FastAPI()

app.include_router(session_router)
app.include_router(chat_router)

INDEX_HTML = (Path(__file__).parent.parent / "index.html").read_text()


@app.get("/", response_class=HTMLResponse)
async def index():
    return INDEX_HTML


@app.get("/scalar")
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url)
