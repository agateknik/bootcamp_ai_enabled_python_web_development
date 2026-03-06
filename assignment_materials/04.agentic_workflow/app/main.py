from scalar_fastapi import get_scalar_api_reference
from fastapi import FastAPI
from dotenv import load_dotenv
from app.modules.threat.schema import ThreatTopicInput
from app.modules.threat.tasks import find_threat_task

load_dotenv()

app = FastAPI()


@app.post("/search-threat")
def do_search_threat(body: ThreatTopicInput):
    find_threat_task.delay(body.topic)
    return {"message": "Processing !"}


@app.get("/scalar")
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
