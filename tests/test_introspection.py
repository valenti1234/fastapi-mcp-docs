from __future__ import annotations

import asyncio
from typing import Any, Dict

from fastapi_mcp_docs.introspection import discover_tools


class ToolObj:
    def __init__(self, name: str):
        self.name = name
        self.description = "d"
        self.inputSchema = {"type": "object"}
        self.outputSchema = {"type": "object"}


def test_discover_tools_from_list_tools():
    class MCP:
        async def list_tools(self):
            return [ToolObj("a"), ToolObj("b")]

    tools = asyncio.run(discover_tools(MCP()))
    assert [t.name for t in tools] == ["a", "b"]
    assert tools[0].input_schema["type"] == "object"


def test_discover_tools_from_tools_dict():
    class MCP:
        def __init__(self):
            self.tools: Dict[str, Any] = {"x": ToolObj("x")}

    tools = asyncio.run(discover_tools(MCP()))
    assert [t.name for t in tools] == ["x"]
