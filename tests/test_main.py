"""Tests for the MCP server CLI and transport selection."""

import pytest
from unittest.mock import patch

from firefly_mcp.main import build_arg_parser, SUPPORTED_TRANSPORTS


class TestArgParser:
    def test_default_transport_is_stdio(self):
        args = build_arg_parser().parse_args([])
        assert args.transport == "stdio"

    def test_supports_streamable_http(self):
        args = build_arg_parser().parse_args(
            ["--transport", "streamable-http", "--host", "127.0.0.1", "--port", "9000"]
        )
        assert args.transport == "streamable-http"
        assert args.host == "127.0.0.1"
        assert args.port == 9000
        assert args.path is None

    def test_supports_custom_path(self):
        args = build_arg_parser().parse_args(["--path", "/custom/mcp"])
        assert args.path == "/custom/mcp"

    @pytest.mark.parametrize("transport", SUPPORTED_TRANSPORTS)
    def test_all_supported_transports_parse(self, transport):
        args = build_arg_parser().parse_args(["--transport", transport])
        assert args.transport == transport

    def test_invalid_transport_rejected(self):
        with pytest.raises(SystemExit):
            build_arg_parser().parse_args(["--transport", "bogus"])

    def test_defaults_host_port(self):
        args = build_arg_parser().parse_args([])
        assert args.host == "0.0.0.0"
        assert args.port == 8000


class TestMainTransportDispatch:
    def test_stdio_default_calls_stdio(self):
        from firefly_mcp import main as main_mod

        args = main_mod.build_arg_parser().parse_args([])
        with patch.object(main_mod.mcp, "run") as mock_run:
            main_mod.main([])
        mock_run.assert_called_once_with(transport="stdio")

    def test_streamable_http_passes_host_port(self):
        from firefly_mcp import main as main_mod

        with patch.object(main_mod.mcp, "run") as mock_run:
            main_mod.main(["--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8080"])
        mock_run.assert_called_once_with(
            transport="streamable-http", host="0.0.0.0", port=8080
        )

    def test_streamable_http_with_custom_path(self):
        from firefly_mcp import main as main_mod

        with patch.object(main_mod.mcp, "run") as mock_run:
            main_mod.main(["--transport", "streamable-http", "--path", "/rpc"])
        assert mock_run.call_args.kwargs["path"] == "/rpc"
