FROM python:3.14-slim

COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

COPY . /app
WORKDIR /app

RUN uv sync

RUN pip install mcpo

COPY entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
