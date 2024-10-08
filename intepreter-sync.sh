#!/bin/bash
source ~/.bash_aliases

mkdir -p /home/python-site-packages
docker run --rm -it -v "$PWD":/app -v /home/python-site-packages:/usr/local/lib/python3.13/site-packages -w /app --network tools-net python:3.13-slim python -m ensurepip
docker run --rm -it -v "$PWD":/app -v /home/python-site-packages:/usr/local/lib/python3.13/site-packages -w /app --network tools-net python:3.13-slim python -m venv .venv
docker run --rm -it -v "$PWD":/app -w /app -e PATH="/app/.venv/bin:$PATH" -e VIRTUAL_ENV="/app/.venv" -e VIRTUAL_ENV_PROMPT=".venv" -e PS1="(.venv) ${PS1:-}" --network tools-net python:3.13-slim python -m ensurepip
docker run --rm -it -v "$PWD":/app -w /app -e PATH="/app/.venv/bin:$PATH" -e VIRTUAL_ENV="/app/.venv" -e VIRTUAL_ENV_PROMPT=".venv" -e PS1="(.venv) ${PS1:-}" --network tools-net python:3.13-slim pip install -r requirements.txt --upgrade
