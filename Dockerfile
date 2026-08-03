FROM python:3.14-slim

COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

COPY . /app
WORKDIR /app

RUN uv sync

RUN pip install mcpo

CMD ["uvx", "--with", "mcp<2", "mcpo", "--host", "0.0.0.0", "--port", "8000", "--", "uv", "run", "firefly-mcp"]
