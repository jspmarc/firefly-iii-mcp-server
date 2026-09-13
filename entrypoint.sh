#!/bin/sh
set -eu

TRANSPORT="${FIREFLY_MCP_TRANSPORT:-streamable-http}"
# Serve at root by default: reverse proxies typically strip their path prefix
# (e.g. Caddy handle_path /firefly/*) and forward the request at "/". Override
# with FIREFLY_MCP_PATH if the server must mount under a sub-path instead.
PATH_ARG="--path ${FIREFLY_MCP_PATH:-/}"

if [ "$TRANSPORT" = "stdio" ]; then
  exec uv run firefly-mcp --transport stdio
fi

exec uv run firefly-mcp \
  --transport streamable-http \
  --host "${FIREFLY_MCP_HOST:-0.0.0.0}" \
  --port "${FIREFLY_MCP_PORT:-8000}" \
  $PATH_ARG
