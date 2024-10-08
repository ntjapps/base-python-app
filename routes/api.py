from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from celery.result import AsyncResult
from worker import celery  # load worker.py

router = APIRouter()


# Celery list worker API


@router.get("/api/v1/workers")
def get_workers():
    workers = celery.control.inspect().stats()
    return JSONResponse(workers)

# Celery get registered tasks API


@router.get("/api/v1/tasks")
def get_task_lists():
    tasks = celery.control.inspect().registered()
    return JSONResponse(tasks)

# Celery get list of active tasks API


@router.get("/api/v1/active-tasks")
def get_active_tasks():
    tasks = celery.control.inspect().active()
    return JSONResponse(tasks)

# Submit task API


class TaskModel(BaseModel):
    task_name: str
    task_args: dict | str | None = None


@router.post("/api/v1/task-submit")
def submit_task(args: TaskModel | None):
    argsDict = args.dict().pop("task_args")
    argsList = list(argsDict.values() if argsDict else [])
    task = celery.send_task(args.task_name, args=argsList)
    return JSONResponse({"task_id": task.id, "task_name": args.task_name, "task_args": argsDict})

# Task status API


@router.get("/api/v1/task-status/{task_id}")
def get_task_status(task_id):
    task = AsyncResult(task_id)
    return JSONResponse({"task_id": task.id, "task_status": task.status, "task_executed": task.ready(), "task_results": task.result})
