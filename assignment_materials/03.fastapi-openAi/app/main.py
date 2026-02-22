from fastapi import FastAPI

from app.modules.gift_idea.router import gift_router

app = FastAPI()

app.include_router(gift_router)


@app.get("/")
def get_index():
    return {"data": "FastAPI integrate AI to give gift idea"}
