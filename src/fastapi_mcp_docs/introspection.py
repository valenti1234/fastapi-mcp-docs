from __future__ import annotations

import inspect
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .schemas import MCPPrompt, MCPResource, MCPSchema, MCPTool


async def _maybe_await(value: Any) -> Any:
    if inspect.isawaitable(value):
        return await value
    return value


def _schema_from_obj(obj: Any) -> Dict[str, Any]:
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    model_json_schema = getattr(obj, "model_json_schema", None)
    if callable(model_json_schema):
        return model_json_schema()
    schema = getattr(obj, "schema", None)
    if callable(schema):
        return schema()
    to_dict = getattr(obj, "dict", None)
    if callable(to_dict):
        d = to_dict()
        if isinstance(d, dict):
            return d
    return {}


def _tool_fields(tool: Any) -> Tuple[Optional[str], Dict[str, Any], Dict[str, Any]]:
    description = getattr(tool, "description", None) or getattr(tool, "doc", None)
    input_schema = (
        getattr(tool, "input_schema", None)
        or getattr(tool, "inputSchema", None)
        or getattr(tool, "parameters", None)
        or getattr(tool, "args_schema", None)
    )
    output_schema = (
        getattr(tool, "output_schema", None)
        or getattr(tool, "outputSchema", None)
        or getattr(tool, "returns_schema", None)
        or getattr(tool, "result_schema", None)
    )
    return description, _schema_from_obj(input_schema), _schema_from_obj(output_schema)


def _prompt_fields(prompt: Any) -> Tuple[Optional[str], Dict[str, Any]]:
    description = getattr(prompt, "description", None) or getattr(prompt, "doc", None)
    input_schema = (
        getattr(prompt, "input_schema", None)
        or getattr(prompt, "inputSchema", None)
        or getattr(prompt, "parameters", None)
    )
    return description, _schema_from_obj(input_schema)


async def discover_schema(mcp: Any) -> MCPSchema:
    tools = await discover_tools(mcp)
    prompts = await discover_prompts(mcp)
    resources = await discover_resources(mcp)
    return MCPSchema(tools=tools, prompts=prompts, resources=resources)


async def discover_tools(mcp: Any) -> List[MCPTool]:
    candidates: Any = []
    if hasattr(mcp, "list_tools") and callable(getattr(mcp, "list_tools")):
        candidates = await _maybe_await(mcp.list_tools())
    elif hasattr(mcp, "get_tools") and callable(getattr(mcp, "get_tools")):
        candidates = await _maybe_await(mcp.get_tools())
    elif hasattr(mcp, "tools"):
        candidates = getattr(mcp, "tools")

    if candidates is None:
        return []

    if isinstance(candidates, dict):
        values = list(candidates.values())
        for name, tool in candidates.items():
            if getattr(tool, "name", None) is None:
                try:
                    setattr(tool, "name", name)
                except Exception:
                    pass
        candidates = values

    out: List[MCPTool] = []
    for t in list(candidates):
        name = getattr(t, "name", None) or getattr(t, "id", None)
        if not name:
            continue
        description, in_schema, out_schema = _tool_fields(t)
        out.append(
            MCPTool(
                name=str(name),
                description=str(description) if description is not None else None,
                input_schema=in_schema,
                output_schema=out_schema,
            )
        )
    out.sort(key=lambda x: x.name)
    return out


async def discover_prompts(mcp: Any) -> List[MCPPrompt]:
    candidates: Any = None
    if hasattr(mcp, "list_prompts") and callable(getattr(mcp, "list_prompts")):
        candidates = await _maybe_await(mcp.list_prompts())
    elif hasattr(mcp, "get_prompts") and callable(getattr(mcp, "get_prompts")):
        candidates = await _maybe_await(mcp.get_prompts())
    elif hasattr(mcp, "prompts"):
        candidates = getattr(mcp, "prompts")

    if not candidates:
        return []

    out: List[MCPPrompt] = []
    for p in list(candidates):
        name = getattr(p, "name", None) or getattr(p, "id", None)
        if not name:
            continue
        description, in_schema = _prompt_fields(p)
        out.append(
            MCPPrompt(
                name=str(name),
                description=str(description) if description is not None else None,
                input_schema=in_schema,
            )
        )
    out.sort(key=lambda x: x.name)
    return out


async def discover_resources(mcp: Any) -> List[MCPResource]:
    candidates: Any = None
    if hasattr(mcp, "list_resources") and callable(getattr(mcp, "list_resources")):
        candidates = await _maybe_await(mcp.list_resources())
    elif hasattr(mcp, "get_resources") and callable(getattr(mcp, "get_resources")):
        candidates = await _maybe_await(mcp.get_resources())
    elif hasattr(mcp, "resources"):
        candidates = getattr(mcp, "resources")

    if not candidates:
        return []

    out: List[MCPResource] = []
    for r in list(candidates):
        uri = getattr(r, "uri", None) or getattr(r, "url", None) or getattr(r, "id", None)
        if not uri:
            continue
        out.append(
            MCPResource(
                uri=str(uri),
                name=getattr(r, "name", None),
                description=getattr(r, "description", None),
            )
        )
    out.sort(key=lambda x: x.uri)
    return out


async def call_tool(mcp: Any, name: str, arguments: Dict[str, Any]) -> Any:
    if hasattr(mcp, "call_tool") and callable(getattr(mcp, "call_tool")):
        return await _maybe_await(mcp.call_tool(name, arguments))
    if hasattr(mcp, "call") and callable(getattr(mcp, "call")):
        return await _maybe_await(mcp.call(name, arguments))
    raise RuntimeError("MCP server does not expose call_tool(...) or call(...)")
