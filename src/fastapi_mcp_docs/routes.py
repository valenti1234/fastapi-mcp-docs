from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse

from .config_export import build_mcp_json
from .introspection import call_tool, discover_schema
from .schemas import MCPDocsConfig, ToolCallRequest, ToolCallResponse
from .ui import render_index_html


def create_mcp_docs_router(*, mcp: Any, config: MCPDocsConfig) -> APIRouter:
    router = APIRouter()

    async def _schema():
        s = await discover_schema(mcp)
        return JSONResponse(s.model_dump(mode="json"))

    @router.get("", include_in_schema=False)
    @router.get("/", include_in_schema=False)
    async def index():
        return HTMLResponse(render_index_html(docs_url=config.docs_url))

    @router.get("/schema", include_in_schema=False)
    async def schema():
        return await _schema()

    @router.get("/config", include_in_schema=False)
    async def export_config():
        return JSONResponse(
            build_mcp_json(
                mcp_url=config.mcp_url, server_name=config.server_name, title="FastAPI MCP server"
            )
        )

    @router.post("/call", include_in_schema=False)
    async def call(req: ToolCallRequest):
        try:
            result = await call_tool(mcp, req.tool, req.arguments)
            return JSONResponse(
                ToolCallResponse(ok=True, tool=req.tool, result=result).model_dump(mode="json")
            )
        except Exception as e:
            return JSONResponse(
                ToolCallResponse(ok=False, tool=req.tool, error=str(e)).model_dump(mode="json"),
                status_code=400,
            )

    return router

