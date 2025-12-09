"""Configuration for Confluence Search Agent"""

import os
from typing import Optional
from google.adk.models.lite_llm import LiteLlm

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
# NOTE: This agent connects ONLY to the MCP server.
# All Confluence credentials are configured on the MCP server side.

CONFLUENCE_MCP_SERVER_URL = os.getenv(
    "CONFLUENCE_MCP_SERVER_URL",
    "http://localhost:3000"  # URL of your MCP server
)

CONFLUENCE_MCP_API_TOKEN = os.getenv(
    "CONFLUENCE_MCP_API_TOKEN",
    ""  # Optional: Auth token for MCP server access
)

# Confluence credentials are NOT needed here.
# They should be configured on the MCP server itself.

# Agent Configuration
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
CITATION_REQUIRED = os.getenv("CITATION_REQUIRED", "true").lower() == "true"
USE_REASONING = os.getenv("USE_REASONING", "true").lower() == "true"
