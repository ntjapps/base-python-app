import os
import time

from celery import Celery

from helpers.apiAuthInterface import getAccessToken

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")
celery.conf.result_expires = 3600
celery.conf.update(result_extended=True)

webhook_endpoint = os.environ.get("WEBHOOK_ENDPOINT")


@celery.task(bind=True, name="test_task")
def test_task(self):
    return {"return": True, "message": "test_task done"}


@celery.task(bind=True, name="test_body_task")
def test_body_task(self, args1: str | None = None, args2: str | None = None, args3: str | None = None):
    body = {"args1": args1, "args2": args2, "args3": args3}
    return {"return": True, "message": "test_body_task done", "body": body}


@celery.task(bind=True, name="test_api_task")
def test_api_task(self):
    # Webhook trigger
    url = webhook_endpoint + "/api/webhook"
    data = {"job_id": job_id}
    token = getAccessToken()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    req = requests.post(url, json=data, headers=headers)
