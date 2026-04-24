from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class MCPTool(BaseModel):
    name: str
    description: Optional[str] = None
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)


class MCPPrompt(BaseModel):
    name: str
    description: Optional[str] = None
    input_schema: Dict[str, Any] = Field(default_factory=dict)


class MCPResource(BaseModel):
    uri: str
    name: Optional[str] = None
    description: Optional[str] = None


class MCPSchema(BaseModel):
    tools: List[MCPTool] = Field(default_factory=list)
    prompts: List[MCPPrompt] = Field(default_factory=list)
    resources: List[MCPResource] = Field(default_factory=list)


class ToolCallRequest(BaseModel):
    tool: str
    arguments: Dict[str, Any] = Field(default_factory=dict)


class ToolCallResponse(BaseModel):
    ok: bool
    tool: str
    result: Any = None
    error: Optional[str] = None


class MCPDocsConfig(BaseModel):
    docs_url: str
    mcp_url: str
    server_name: str = "mcp"

