Short, focused guidance for AI coding agents working on this repository.

Repository overview
- FastAPI web app: `main.py` (includes `routes/api.py`). Healthcheck at `/app/healthcheck`.
- Background workers: `worker.py` (Celery instance) + `worker-config.py` (Celery config). Tasks live in `jobs/*.py`.
- Helpers for external integration in `helpers/` (IMAP, OAuth/API client, Laravel-format logger payloads).
- DB model: `models/ServerLog.py` and DB connection helper in `database/config.py`.

Important constraints
- Keep web and worker responsibilities separate. Celery jobs must NOT call the main app back (see comment in `jobs/logger_job.py`) — this prevents infinite callback loops.
- Celery uses JSON serialization and PostgreSQL result backend. Tasks should accept JSON-serializable args.
- `worker-config.py` expects a `.env` to be present (it will symlink `/app/.env` to `.env` if missing). Do not hardcode secrets in code.

Patterns to follow (with concrete examples)
- Declaring tasks: use `from worker import celery` and decorate with:
  @celery.task(name="my_task_name")
  (see `jobs/test_job.py`, `jobs/logger_job.py`)
- Submitting tasks programmatically: `celery.send_task("task_name", args=[...])` (see `run.py`). The API endpoint `/api/v1/task-submit` in `routes/api.py` mirrors this.
- Writing logs to DB: construct a Laravel-style payload using `helpers/laravelDbLoggerInterface.laravel_log_payload(...)` and submit to `log_db_task` (see `jobs/logger_job.py`).
- SQLAlchemy usage: `models/ServerLog.py` exposes `ServerLogSession()` to obtain a session; jobs use `insert()` and `session.commit()`.

Developer workflows
- Run the FastAPI app locally: python `main.py` (it runs Uvicorn when executed as __main__).
- Trigger demo tasks: python `run.py` will send example tasks to the Celery worker.
- Run tests: from project root run `pytest -q` (tests are located under `tests/`).

Conventions & gotchas
- Logging: the worker sets a custom `LaravelFormatter` in `worker.py`. Respect that format if adding handlers or changing log output.
- Task naming: tasks are explicitly named (`name="..."`) — use those names when calling `send_task` or via the API.
- Avoid importing or executing heavy startup logic at module import time in workers; prefer lazy imports inside task functions.

Integration points to inspect before edits
- `worker-config.py` — RabbitMQ (RABBITMQ_* env vars) and Postgres (DB_*) settings.
- `helpers/apiAuthInterface.py` — OAuth client credentials flow used by tasks that call the main app.
- `routes/api.py` — task inspection and task-submit endpoints; useful reference for how tasks are expected to be invoked.

When changing public behavior
- Add or update tests under `tests/` and run `pytest -q`.
- Update environment variable docs (README.md) if you introduce new env vars.

If anything is unclear, ask the maintainer for the current `.env` conventions, RabbitMQ and Postgres endpoints, and expected production logging sink.

Files to read first: `main.py`, `routes/api.py`, `worker.py`, `worker-config.py`, `jobs/logger_job.py`, `helpers/laravelDbLoggerInterface.py`, `models/ServerLog.py`, `database/config.py`.
