FROM ghcr.io/ntjapps/python-custom:latest

ENV SENTRY_PYTHON_DSN=""

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY . .

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
