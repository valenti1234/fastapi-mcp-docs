from __future__ import annotations

from typing import Any, Dict, List

from fastapi import FastAPI

from fastapi_mcp_docs import mount_mcp_docs


class Tool:
    def __init__(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        output_schema: Dict[str, Any],
    ):
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.output_schema = output_schema


class DemoMCP:
    def __init__(self):
        self._tools: List[Tool] = [
            Tool(
                name="add",
                description="Add two numbers.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "a": {"type": "number"},
                        "b": {"type": "number"},
                    },
                    "required": ["a", "b"],
                },
                output_schema={"type": "number"},
            ),
            Tool(
                name="echo",
                description="Echo back the provided payload.",
                input_schema={"type": "object"},
                output_schema={"type": "object"},
            ),
        ]

    def list_tools(self):
        return self._tools

    def call_tool(self, name: str, arguments: Dict[str, Any]):
        if name == "add":
            return float(arguments.get("a", 0)) + float(arguments.get("b", 0))
        if name == "echo":
            return arguments
        raise ValueError(f"Unknown tool: {name}")


app = FastAPI(title="fastapi-mcp-docs example")
mcp = DemoMCP()

mount_mcp_docs(app, mcp, docs_url="/mcp-docs", mcp_url="/mcp")

