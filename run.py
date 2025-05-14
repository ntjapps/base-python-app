import sys

from celery import Celery
from helpers.laravelDbLoggerInterface import laravel_log_payload


def runScripts():
    print("Running scripts")
    # Example of how to use the laravel_log_payload function
    payload = laravel_log_payload(
        "This is a test message", level="info", context="Test context")
    print("Generated payload:", payload)


if __name__ == "__main__":
    runScripts(*sys.argv[1:])
