from worker import celery

from helpers.apiAuthInterface import getAccessToken, postApiEndpoint


@celery.task(name="celery_test_task")
def celery_test_task():
    return {"return": True, "message": "test_task done"}


@celery.task(name="celery_test_sentry_task")
def celery_test_task():
    raise Exception("Raised Exception on purpose to send it to Bugsink")


@celery.task(name="celery_test_body_task")
def celery_test_body_task(args1: str | None = None, args2: str | None = None, args3: str | None = None):
    body = {"args1": args1, "args2": args2, "args3": args3}
    return {"return": True, "message": "test_body_task done", "body": body}


@celery.task(name="celery_test_api_task")
def celery_test_api_task():
    req = postApiEndpoint("api/v1/rabbitmq/test-rabbitmq", scope="rabbitmq")

    if req.status_code != 200:
        raise Exception("test_api_task failed with status code: " +
                        str(req.status_code) + " and message: " + req.text)
    else:
        return {"return": True, "message": "test_api_task done", "body": req.json(), "status_code": req.status_code}
