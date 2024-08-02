from fastapi import FastAPI
import sentry_sdk
import os
from fastapi.responses import JSONResponse
from routes import api

env_dsn_sentry = os.getenv("SENTRY_PYTHON_DSN", None)

sentry_sdk.init(
    dsn=env_dsn_sentry,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=0.01,
)

app = FastAPI()

# Health check API


@app.get("/app/healthcheck")
def read_root():
    return JSONResponse({"status": "ok"})


# Import routes
app.include_router(api.router)
