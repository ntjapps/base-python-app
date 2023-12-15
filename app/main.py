from fastapi import FastAPI
import sentry_sdk
import os

env_dsn_sentry = os.getenv("SENTRY_PYTHON_DSN", None)

sentry_sdk.init(
    dsn=env_dsn_sentry,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=0.1,
)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
