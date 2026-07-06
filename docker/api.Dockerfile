FROM python:3.11-slim

WORKDIR /app

COPY src /app/src
COPY docker /app/docker

RUN pip install --no-cache-dir fastapi uvicorn

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uvicorn", "deepcore.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
