#!/bin/sh
set -eu

TRANSPORT="${FIREFLY_MCP_TRANSPORT:-streamable-http}"

if [ "$TRANSPORT" = "stdio" ]; then
  exec uv run firefly-mcp --transport stdio
fi

exec uv run firefly-mcp \
  --transport streamable-http \
  --host "${FIREFLY_MCP_HOST:-0.0.0.0}" \
  --port "${FIREFLY_MCP_PORT:-8000}" \
  ${FIREFLY_MCP_PATH:+--path "$FIREFLY_MCP_PATH"}
