# pull official base image
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# set working directory
WORKDIR /usr/src/

ENV UV_NO_DEV=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock ./

# install system dependencies
RUN uv sync --locked --no-install-project

COPY app app
COPY alembic.ini ./

RUN uv sync --locked --no-dev

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips=*"]
