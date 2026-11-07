# Dockerfile


FROM python:3.13-slim-bookworm as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


FROM python:3.13-slim-bookworm

RUN mkdir -p /app/backend_engineer/staticfiles

WORKDIR /app

RUN addgroup --system app && adduser --system --group app && chown -R app /app

RUN apt-get update

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

ENV SENTENCE_TRANSFORMERS_MODEL=Qwen/Qwen3-Embedding-0.6B
ENV SENTENCE_TRANSFORMERS_HOME=/app/backend_engineer/embedding_models

COPY backend_engineer/backend_services/download_model.py /app/backend_engineer/backend_services/download_model.py

RUN python /app/backend_engineer/backend_services/download_model.py

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# USER app