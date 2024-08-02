FROM python:slim

ENV SENTRY_PYTHON_DSN=""

RUN apt-get update && apt-get install -y gcc musl-dev && mkdir /app

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get autoremove -y gcc musl-dev

COPY . .

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
