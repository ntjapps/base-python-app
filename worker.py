from celery import Celery, signals
import logging

celery = Celery(__name__)
celery.config_from_object("worker-config")

celery.autodiscover_tasks(["jobs.test_job", "jobs.logger_job"])


class LaravelFormatter(logging.Formatter):
    def format(self, record):
        level = record.levelname.lower()
        time = self.formatTime(record, "%Y-%m-%d %H:%M:%S.%f")
        return f"[{time}] local.{level}: {record.getMessage()}"


formatter = LaravelFormatter()

handler = logging.StreamHandler()
handler.setFormatter(formatter)

root_logger = logging.getLogger()
root_logger.handlers = []
root_logger.addHandler(handler)
root_logger.setLevel(logging.INFO)
