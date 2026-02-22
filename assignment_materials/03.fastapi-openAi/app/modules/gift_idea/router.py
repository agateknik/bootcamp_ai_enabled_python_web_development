import markdown
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

from app.modules.gift_idea.schema import Gift_Idea
from app.utils.openai import client

from .prompt import SYSTEM_PROMPT

template = Jinja2Templates("app/templates")
gift_router = APIRouter(prefix="/gift-idea")


@gift_router.get("")
def get_idea(request: Request):
    return template.TemplateResponse("index.html", {"request": request})


@gift_router.post("")
def create_idea(request: Request, gift_idea=Form(None), budget=Form(None)):
    res = client.chat.completions.parse(
        model="openai/gpt-5.1-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"gift idea: {gift_idea}, budget: {budget}"},
        ],
        extra_body={"reasoning": {"enabled": True}},
        response_format=Gift_Idea,
    )
    result = res.choices[0].message.parsed
    return template.TemplateResponse("gift-idea.html", {"request": request, "gift": result})
