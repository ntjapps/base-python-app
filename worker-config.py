# Configuration for Celery
import os
from dotenv import load_dotenv

# Check if .env link is available
if not os.path.exists(".env"):
    print(".env file is not available")

    # Create symbolic link from /var/www/vhosts/localhost/.env to .env
    os.symlink("/var/www/vhosts/localhost/.env", ".env")

    # Check if .env link is available
    if not os.path.exists(".env"):
        print(".env file still is not available, terminating..")
        exit(1)

# Load environment variables
load_dotenv()

broker_url = "pyamqp://{0}:{1}@{2}:{3}/{4}".format(os.getenv("RABBITMQ_USER"), os.getenv(
    "RABBITMQ_PASSWORD"), os.getenv("RABBITMQ_HOST"), os.getenv("RABBITMQ_PORT"), os.getenv("RABBITMQ_VHOST"))

result_backend = "db+postgresql+psycopg://{0}:{1}@{2}:{3}/{4}".format(os.getenv("DB_USERNAME"), os.getenv(
    "DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_DATABASE"))

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

timezone = 'UTC'
enable_utc = True
track_started = True

worker_concurrency = 4

task_queues = {
    'celery': {
        'exchange': 'celery',
        'routing_key': 'celery',
    },

    'logger': {
        'exchange': 'celery',
        'routing_key': 'logger',
    },
}

default_queue = 'celery'
