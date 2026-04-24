# fastapi-mcp-docs

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-%3E%3D3.9-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-%3E%3D0.110-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-valenti1234%2Ffastapi--mcp--docs-181717.svg?logo=github&logoColor=white)](https://github.com/valenti1234/fastapi-mcp-docs)

Embed an interactive MCP documentation UI inside a FastAPI app (inspired by MCP Inspector), mounted at `/mcp-docs`.

## Install

```bash
pip install fastapi-mcp-docs
```

For tests:

```bash
pip install "fastapi-mcp-docs[test]"
```

## Usage

```python
from fastapi import FastAPI
from fastapi_mcp_docs import mount_mcp_docs

app = FastAPI()

# `mcp` can be a FastMCP/MCP server object that exposes tools (and optionally prompts/resources)
# and supports tool calling via `call_tool(...)` / `call(...)`.
mcp = ...

mount_mcp_docs(app, mcp, docs_url="/mcp-docs", mcp_url="/mcp")
```

Then open:

- `GET /mcp-docs` for the UI
- `GET /mcp-docs/schema` for discovered tools/prompts/resources
- `POST /mcp-docs/call` to call a tool from the UI
- `GET /mcp-docs/config` to export an `mcp.json` snippet for clients

## Notes on compatibility

`fastapi-mcp-docs` aims to work with different MCP server implementations by using light introspection:

- Discovery: tries `list_tools()` / `tools`, `list_prompts()` / `prompts`, `list_resources()` / `resources`
- Calling: tries `call_tool(name, arguments)` then `call(name, arguments)`

If your server uses different method/attribute names, you can wrap it in a small adapter that provides the above methods.

## Example app

Run:

```bash
pip install "fastapi-mcp-docs[example]"
python -m uvicorn examples.app:app --reload
```

Then open `http://localhost:8000/mcp-docs`.
