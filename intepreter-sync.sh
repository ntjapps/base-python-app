#!/bin/bash
source ~/.bash_aliases

mkdir -p /home/python-site-packages
docker run --rm -it -v "$PWD":/app -v /home/python-site-packages:/usr/local/lib/python3.12/site-packages -w /app --network tools-net python:slim python -m ensurepip
docker run --rm -it -v "$PWD":/app -v /home/python-site-packages:/usr/local/lib/python3.12/site-packages -w /app --network tools-net python:slim pip install -r requirements.txt --upgrade
