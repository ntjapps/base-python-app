import sys

from worker import celery
from helpers.laravelDbLoggerInterface import laravel_log_payload


def runScripts():
    print("Running scripts")
    celery.send_task("celery_test_sentry_task")
    print("Scripts finished")


if __name__ == "__main__":
    runScripts(*sys.argv[1:])
