from __future__ import annotations

from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_mcp_docs import mount_mcp_docs


class Tool:
    def __init__(self, name: str, description: str, input_schema: Dict[str, Any], output_schema: Dict[str, Any]):
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.output_schema = output_schema


class DummyMCP:
    def __init__(self):
        self.tools: List[Tool] = [
            Tool(
                name="ping",
                description="Return pong.",
                input_schema={"type": "object", "properties": {}},
                output_schema={"type": "object"},
            )
        ]

    def call_tool(self, name: str, arguments: Dict[str, Any]):
        if name != "ping":
            raise ValueError("unknown tool")
        return {"pong": True, "arguments": arguments}


def test_ui_and_schema_and_call():
    app = FastAPI()
    mount_mcp_docs(app, DummyMCP(), docs_url="/mcp-docs", mcp_url="/mcp")
    client = TestClient(app)

    r = client.get("/mcp-docs")
    assert r.status_code == 200
    assert "MCP Docs" in r.text

    r = client.get("/mcp-docs/schema")
    assert r.status_code == 200
    payload = r.json()
    assert "tools" in payload
    assert payload["tools"][0]["name"] == "ping"

    r = client.post("/mcp-docs/call", json={"tool": "ping", "arguments": {"x": 1}})
    assert r.status_code == 200
    out = r.json()
    assert out["ok"] is True
    assert out["tool"] == "ping"
    assert out["result"]["pong"] is True
    assert out["result"]["arguments"]["x"] == 1


def test_export_config():
    app = FastAPI()
    mount_mcp_docs(app, DummyMCP(), docs_url="/mcp-docs", mcp_url="/mcp", server_name="local")
    client = TestClient(app)

    r = client.get("/mcp-docs/config")
    assert r.status_code == 200
    cfg = r.json()
    assert "mcpServers" in cfg
    assert "local" in cfg["mcpServers"]
    assert "url" in cfg["mcpServers"]["local"]

