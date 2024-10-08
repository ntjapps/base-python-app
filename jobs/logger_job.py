import os
import json
from datetime import datetime
from sqlalchemy import insert
import uuid_utils as uuid

from worker import celery
from models.ServerLog import ServerLogModel, ServerLogSession

# This job MUST NOT CALLBACK to Main Application to prevent infinite loop


@celery.task(bind=True, name="log_db_task")
def log_db_task(self, args1: str | None):
    class LoggerInterfaceModel:
        message: str
        channel: str
        level: str
        level_name: str
        datetime: str
        context: str
        extra: str

    payload: LoggerInterfaceModel = json.loads(args1) if args1 else None

    if payload is not None:
        with ServerLogSession() as session:
            session.execute(insert(ServerLogModel), [
                {
                    "id": str(uuid.uuid7()),
                    "message": payload['message'],
                    "channel": payload['channel'],
                    "level": payload['level'],
                    "level_name": payload['level_name'],
                    "datetime": payload['datetime'],
                    "context": payload['context'],
                    "extra": payload['extra'],
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
            ])
            session.commit()
            session.close()
    else:
        print("No payload")

    return {"return": True, "message": "log_db_task done"}
