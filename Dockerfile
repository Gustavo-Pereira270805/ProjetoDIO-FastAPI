FROM python:3.13-slim as builder

WORKDIR /app

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true 

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root --no-dev

FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /app/.venv ./.venv

COPY ProjetoDIO_fastapi/ ./workout_api

COPY main.py .

EXPOSE 8000

CMD ["./.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]