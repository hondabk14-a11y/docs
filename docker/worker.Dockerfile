FROM python:3.11-slim

WORKDIR /app

COPY src /app/src
COPY docker /app/docker

RUN pip install --no-cache-dir redis fastapi uvicorn

ENV PYTHONPATH=/app/src

CMD ["python", "-m", "deepcore.workers.consumer"]
