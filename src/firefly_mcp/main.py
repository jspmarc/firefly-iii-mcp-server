import argparse
import logging
import os

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastmcp import FastMCP
from firefly_mcp.tools.main import create_mcp_server
from firefly_mcp.models.app import AppContext

SUPPORTED_TRANSPORTS = ("stdio", "streamable-http")


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context."""
    # Initialize on startup
    logging.info("Starting up...")
    try:
        yield AppContext()
    finally:
        logging.info("Shutting down...")


mcp = create_mcp_server(app_lifespan)


def get_mcp_server() -> FastMCP:
    """Get the configured MCP server instance."""
    return mcp


def build_arg_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser for the Firefly MCP server."""
    parser = argparse.ArgumentParser(
        prog="firefly-mcp",
        description="Firefly III Model Context Protocol (MCP) server.",
    )
    parser.add_argument(
        "--transport",
        choices=SUPPORTED_TRANSPORTS,
        default="stdio",
        help=(
            "MCP transport to use. Use 'stdio' for local clients (Claude "
            "Desktop, Cursor, etc.) and 'streamable-http' to expose the "
            "server as a Streamable HTTP web service. (default: %(default)s)"
        ),
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host/interface to bind when using an HTTP transport. (default: %(default)s)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind when using an HTTP transport. (default: %(default)s)",
    )
    parser.add_argument(
        "--path",
        default=None,
        help="Base path for the HTTP transport endpoint (e.g. /mcp).",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Main entry point for the MCP server.

    Supports both the stdio transport (local clients) and the
    Streamable HTTP transport (network/web clients).
    """
    args = build_arg_parser().parse_args(argv)

    logging.basicConfig(
        level=logging.getLevelName(os.getenv("FIREFLY_LOG_LEVEL", "INFO")),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if args.transport == "streamable-http":
        kwargs: dict = {"transport": "streamable-http", "host": args.host, "port": args.port}
        if args.path:
            kwargs["path"] = args.path
        logging.info(
            "Starting Firefly MCP server over Streamable HTTP transport "
            "on http://%s:%s%s",
            args.host,
            args.port,
            args.path or "",
        )
        mcp.run(**kwargs)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
