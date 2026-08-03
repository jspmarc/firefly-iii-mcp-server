#!/bin/sh
exec uvx --with "mcp<2" mcpo \
  --host 0.0.0.0 \
  --port 8000 \
  --env FIREFLY_API_URL="$FIREFLY_API_URL" \
  --env FIREFLY_API_TOKEN="$FIREFLY_API_TOKEN" \
  --env FIREFLY_ENABLED_ENTITIES="$FIREFLY_ENABLED_ENTITIES" \
  --env FIREFLY_DIRECT_MODE="$FIREFLY_DIRECT_MODE" \
  -- uv run firefly-mcp