import sys

from worker import celery
from helpers.laravelDbLoggerInterface import laravel_log_payload


def runScripts():
    print("Running scripts")
    # Example of how to use the laravel_log_payload function
    payload = laravel_log_payload(
        "This is a test message", level="info", context={"message": "Test context"})
    celery.send_task("log_db_task", args=[payload])
    print("Scripts finished")


if __name__ == "__main__":
    runScripts(*sys.argv[1:])
