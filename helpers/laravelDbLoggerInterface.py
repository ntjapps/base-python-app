from datetime import datetime
import uuid_utils as uuid
import json

def laravel_log_payload(message: str, level: str = "info", context: dict = None, extra: dict = None) -> dict:
    """
    Returns a dict in Laravel log format using Monolog/PSR-3 levels.
    :param message: Log message
    :param level: Log level (e.g., 'info', 'error', 'warning', 'notice', etc.)
    :param context: Context dict (will be converted to JSON string or [])
    :param extra: Extra dict (will be converted to JSON string or [])
    """
    level_name = level.upper()
    level_num = {
        "debug": 100,
        "info": 200,
        "notice": 250,
        "warning": 300,
        "error": 400,
        "critical": 500,
        "alert": 550,
        "emergency": 600
    }.get(level.lower(), 200)
    now = datetime.now()
    datetime_str = now.strftime("%Y-%m-%d %H:%M:%S") + f".{now.microsecond // 1000:03d}"
    context_str = json.dumps(context) if context else "[]"
    extra_str = json.dumps(extra) if extra else "[]"
    return {
        "id": str(uuid.uuid7()),
        "message": message,
        "channel": "celery",
        "level": str(level_num),
        "level_name": level_name,
        "datetime": datetime_str,
        "context": context_str,
        "extra": extra_str,
        "created_at": datetime_str,
        "updated_at": datetime_str,
    }
