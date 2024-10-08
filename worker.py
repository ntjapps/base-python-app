from celery import Celery

celery = Celery(__name__)
celery.config_from_object("worker-config")

celery.autodiscover_tasks(["jobs.test_job", "jobs.logger_job"])
