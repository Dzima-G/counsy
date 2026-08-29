# pull official base image
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

# set working directory
WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock ./

FROM base AS dev

RUN uv sync --locked
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


FROM base AS prod

ENV UV_NO_DEV=1

RUN uv sync --locked --no-dev
COPY app app
COPY alembic.ini ./
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips=*"]
