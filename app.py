from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json
import random
from pathlib import Path

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DATA_PATH = Path("data/questions.json")

def load_data() -> dict:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    data = load_data()
    topics = sorted(data.keys())
    return templates.TemplateResponse("index.html", {"request": request, "topics": topics})

@app.get("/topic/{topic}", response_class=HTMLResponse)
def topic_page(request: Request, topic: str):
    data = load_data()
    if topic not in data:
        return RedirectResponse(url="/", status_code=302)

    qa = random.choice(data[topic])
    return templates.TemplateResponse(
        "topic.html",
        {"request": request, "topic": topic, "qa": qa}
    )

@app.get("/topic/{topic}/next")
def next_question(topic: str):
    # simple redirect that reloads with a new random question
    return RedirectResponse(url=f"/topic/{topic}", status_code=302)
