from __future__ import annotations

from typing import Any, Dict, Optional


def build_mcp_json(
    *,
    mcp_url: str,
    server_name: str = "mcp",
    title: Optional[str] = None,
) -> Dict[str, Any]:
    url = mcp_url
    if not (url.startswith("http://") or url.startswith("https://")):
        url = f"http://localhost:8000{mcp_url if mcp_url.startswith('/') else '/' + mcp_url}"

    server: Dict[str, Any] = {"url": url}
    if title:
        server["title"] = title

    return {"mcpServers": {server_name: server}}

