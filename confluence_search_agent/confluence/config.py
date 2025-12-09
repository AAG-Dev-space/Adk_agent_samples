"""Configuration for Confluence Search Agent"""

import os
from typing import Optional
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams

# Get model configuration from environment variables
AGENT_MODEL = os.getenv("AGENT_MODEL", "gemini/gemini-2.5-flash-lite")
AGENT_API_KEY = os.getenv("AGENT_API_KEY", "sk-4444")
AGENT_API_BASE = os.getenv("AGENT_API_BASE", "http://localhost:4444")

# Create LiteLLM model
# Note: custom_llm_provider="openai" forces OpenAI-compatible API call to proxy
# api_base should include /v1 for OpenAI-compatible endpoints
llm_model = LiteLlm(
    model=AGENT_MODEL,
    api_key=AGENT_API_KEY,
    api_base=f"{AGENT_API_BASE}/v1" if not AGENT_API_BASE.endswith("/v1") else AGENT_API_BASE,
    custom_llm_provider="openai",
)

# Confluence MCP Server Configuration
# Uses ADK's official McpToolset with streamable-http (SSE) connection
# Reference: https://google.github.io/adk-docs/tools-custom/mcp-tools/

CONFLUENCE_MCP_SERVER_URL = os.getenv(
    "CONFLUENCE_MCP_SERVER_URL",
    "http://localhost:3000/mcp"  # Dummy MCP server endpoint
)

# Create MCP toolset for Confluence
# Uses streamable-http (SSE) connection to MCP server
# All Confluence credentials are managed by the MCP server itself
confluence_mcp_toolset = McpToolset(
    connection_params=SseConnectionParams(url=CONFLUENCE_MCP_SERVER_URL),
)

# Agent Configuration
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
CITATION_REQUIRED = os.getenv("CITATION_REQUIRED", "true").lower() == "true"
USE_REASONING = os.getenv("USE_REASONING", "true").lower() == "true"
