import sys

from celery import Celery


def runScripts():
    print("Running scripts")
    app = Celery(
        __name__, broker='pyamqp://queueuser:queuepass@base_python_rabbitmq:5672/queuevhost')
    app.send_task('test_api_task')


if __name__ == "__main__":
    runScripts(*sys.argv[1:])
