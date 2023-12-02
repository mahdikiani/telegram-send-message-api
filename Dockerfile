FROM python:3.11-slim

WORKDIR "/app"

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt --no-cache-dir
