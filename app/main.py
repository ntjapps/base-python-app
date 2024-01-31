from fastapi import FastAPI, Body, Request
import sentry_sdk
import os
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from worker import create_task
from celery.result import AsyncResult

env_dsn_sentry = os.getenv("SENTRY_PYTHON_DSN", None)

sentry_sdk.init(
    dsn=env_dsn_sentry,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=0.01,
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/home")
def home(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})


@app.post("/tasks", status_code=201)
def run_task(payload=Body(...)):
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@app.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)
