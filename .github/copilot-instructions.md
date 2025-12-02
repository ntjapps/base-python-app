
<!--
  Model instructions for AI agents in base-python-app.
  Keep it short and actionable for quick contributions.
-->

# AI assistant instructions for base-python-app (FastAPI + Celery)

Purpose: Help an AI agent be productive and safe in a project with a FastAPI app and Celery workers. Emphasize separation between web and worker responsibilities, data safety, and testing.

Project snapshot
- FastAPI app: `main.py` (routes in `routes/api.py`) with healthcheck at `/app/healthcheck`.
- Celery worker: `worker.py` + `worker-config.py`; tasks live in `jobs/*.py`.
- Helpers: `helpers/` for IMAP, OAuth, and Laravel-format logger payloads.
- DB model: `models/ServerLog.py`; config in `database/config.py`.

Quick workflows (common commands)
- Run API locally: `python main.py` (starts Uvicorn)
- Trigger demo tasks: `python run.py`
- Run tests: `pytest -q`

Key patterns & constraints
- Do not let Celery tasks call the main app (use API calls with OAuth if needed) to avoid infinite loops. See comment in `jobs/logger_job.py`.
- Celery tasks must accept JSON-serializable arguments; Celery uses JSON serialization and Postgres result backend.
- `worker-config.py` expects an `.env` (symlinks `/app/.env` if missing). Never hardcode secrets; use env and secure vaults.
- Avoid heavy module imports at task import-time; use lazy imports within tasks.

Typical idioms & references
- Declaring a task: import celery via `from worker import celery` and use `@celery.task(name="my_task_name")`.
- Submitting tasks: `celery.send_task("task_name", args=[...])` or use the `/api/v1/task-submit` endpoint.
- Logging to DB: construct payload via `helpers/laravelDbLoggerInterface.laravel_log_payload(...)` and use `log_db_task`.
- DB sessions: use `models/ServerLog.ServerLogSession()` for SQLAlchemy sessions and commit changes.

Tests & CI rules
- Add/modify tests under `tests/` and run `pytest -q`. Ensure tasks are mockable and non-destructive for CI.
- If you update environment variables or credentials the app expects (RabbitMQ, Postgres), update README and document how CI/devs get these values.

Security & safety
- Avoid storing secrets in code. If you need a temporary secret for local runs, note it in README but keep it out of commits.
- Ensure Celery tasks are idempotent where possible and always validate/normalize incoming payloads.

Files to inspect first
- `main.py`, `routes/api.py`, `worker.py`, `worker-config.py`, `jobs/`, `helpers/`, `models/ServerLog.py`, `database/config.py`.

If in doubt
- Ask the repo owner for `.env` conventions, queue and DB endpoints, and production logging sinks.

Feedback
- If any part of these instructions is unclear, tell me the task you expect the AI to perform and I'll expand or adjust these instructions.
