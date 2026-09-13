FROM python:3.14-slim

COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

COPY . /app
WORKDIR /app

RUN uv sync

COPY entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/entrypoint.sh

# Default to the Streamable HTTP transport; supports stdio via FIREFLY_MCP_TRANSPORT.
ENV FIREFLY_MCP_TRANSPORT=streamable-http
EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]
