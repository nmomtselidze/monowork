# syntax=docker/dockerfile:1.7
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (cache efficient)
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy source
COPY ai_sanatorium_scheduler /app/ai_sanatorium_scheduler

EXPOSE 8081

CMD ["uvicorn", "ai_sanatorium_scheduler.api.main:app", "--host", "0.0.0.0", "--port", "8081"]
