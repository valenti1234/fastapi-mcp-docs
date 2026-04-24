from __future__ import annotations

from typing import Any

from fastapi import FastAPI

from .routes import create_mcp_docs_router
from .schemas import MCPDocsConfig


def mount_mcp_docs(
    app: FastAPI,
    mcp: Any,
    *,
    docs_url: str = "/mcp-docs",
    mcp_url: str = "/mcp",
    server_name: str = "mcp",
) -> None:
    docs_url = docs_url if docs_url.startswith("/") else f"/{docs_url}"
    mcp_url = mcp_url if mcp_url.startswith("/") else f"/{mcp_url}"

    config = MCPDocsConfig(docs_url=docs_url, mcp_url=mcp_url, server_name=server_name)
    router = create_mcp_docs_router(mcp=mcp, config=config)
    app.include_router(router, prefix=docs_url)

