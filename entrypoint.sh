#!/bin/sh
# Start the Firefly III MCP server.
#
# Defaults to the Streamable HTTP transport so the container can be reached
# directly by MCP clients over the network (no external proxy needed). For
# local clients you can switch to stdio with FIREFLY_MCP_TRANSPORT=stdio.
#
# Configuration: the server reads all settings directly from the environment
# (FIREFLY_API_URL, FIREFLY_API_TOKEN, FIREFLY_ENABLED_ENTITIES,
# FIREFLY_DIRECT_MODE, FIREFLY_LOG_LEVEL, ...) via os.getenv at startup. The
# container process IS the server, so every env var set for the container is
# inherited automatically - nothing needs to be forwarded explicitly.
#
# Additional launcher env:
#   FIREFLY_MCP_TRANSPORT - "streamable-http" (default) or "stdio"
#   FIREFLY_MCP_HOST      - bind host (default: 0.0.0.0)
#   FIREFLY_MCP_PORT      - bind port (default: 8000)
#   FIREFLY_MCP_PATH      - optional base path for the MCP endpoint
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
