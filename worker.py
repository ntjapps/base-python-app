from celery import Celery, signals
import os
import sentry_sdk
import logging

celery = Celery(__name__)
celery.config_from_object("worker-config")

celery.autodiscover_tasks(["jobs.test_job", "jobs.logger_job"])

webhook_endpoint = os.getenv("APP_URL")
celry_dsn = os.getenv("CELERY_DSN")


class LaravelFormatter(logging.Formatter):
    def format(self, record):
        level = record.levelname.lower()
        time = self.formatTime(record, "%Y-%m-%d %H:%M:%S.%f")
        return f"[{time}] local.{level}: {record.getMessage()}"


formatter = LaravelFormatter()

handler = logging.StreamHandler()
handler.setFormatter(formatter)

root_logger = logging.getLogger()
root_logger.handlers = []  # Remove default handlers
root_logger.addHandler(handler)
root_logger.setLevel(logging.INFO)


@signals.celeryd_init.connect
def init_sentry(**_kwargs):
    sentry_sdk.init(
        dsn=celry_dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )
