"""MCP Client for Confluence Server Integration

This module handles the actual communication with the Confluence MCP server.
References:
- ADK MCP Documentation: https://github.com/google/adk-docs/blob/main/docs/mcp/index.md
- MCP Protocol: https://github.com/google/adk-docs/blob/main/docs/tools/mcp-tools.md
"""

import os
import json
from typing import Dict, Any, Optional, List
import httpx
from datetime import datetime


class ConfluenceMCPClient:
    """Client for communicating with Confluence MCP Server.

    This client ONLY communicates with the MCP server.
    The MCP server handles all Confluence connectivity.

    Configuration:
    - CONFLUENCE_MCP_SERVER_URL: URL of your MCP server (e.g., http://mcp-server:3000)
    - CONFLUENCE_MCP_API_TOKEN: Optional auth token for MCP server

    The MCP server itself needs these configured internally:
    - CONFLUENCE_BASE_URL
    - CONFLUENCE_USERNAME
    - CONFLUENCE_API_TOKEN
    """

    def __init__(
        self,
        mcp_server_url: Optional[str] = None,
        api_token: Optional[str] = None,
        timeout: int = 30
    ):
        """Initialize MCP client.

        Args:
            mcp_server_url: URL of the Confluence MCP server
                           This is the ONLY endpoint we connect to.
                           All Confluence operations go through this MCP server.
            api_token: Optional authentication token for MCP server
            timeout: Request timeout in seconds
        """
        self.server_url = mcp_server_url or os.getenv(
            "CONFLUENCE_MCP_SERVER_URL",
            "http://localhost:3000"  # Default MCP server port
        )
        self.api_token = api_token or os.getenv("CONFLUENCE_MCP_API_TOKEN", "")
        self.timeout = timeout

        # Initialize HTTP client - ONLY connects to MCP server
        headers = {"Content-Type": "application/json"}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"

        self.client = httpx.AsyncClient(
            base_url=self.server_url,
            headers=headers,
            timeout=timeout
        )

    async def call_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Call an MCP tool on the server.

        Args:
            tool_name: Name of the MCP tool to call
            arguments: Tool arguments as dictionary

        Returns:
            Tool response as dictionary

        Raises:
            httpx.HTTPError: If the request fails
        """
        # MCP protocol format
        request_payload = {
            "jsonrpc": "2.0",
            "id": self._generate_request_id(),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }

        try:
            response = await self.client.post(
                "/mcp/v1/call",
                json=request_payload
            )
            response.raise_for_status()

            result = response.json()

            # Handle MCP error responses
            if "error" in result:
                error = result["error"]
                raise MCPError(
                    f"MCP Error {error.get('code')}: {error.get('message')}"
                )

            return result.get("result", {})

        except httpx.HTTPError as e:
            print(f"MCP Client HTTP Error: {e}")
            raise
        except Exception as e:
            print(f"MCP Client Error: {e}")
            raise

    async def search_content(
        self,
        query: str,
        space_key: Optional[str] = None,
        max_results: int = 5
    ) -> Dict[str, Any]:
        """Search Confluence content via MCP.

        Args:
            query: Search query
            space_key: Optional space to search in
            max_results: Maximum results to return

        Returns:
            Search results dictionary
        """
        arguments = {
            "query": query,
            "limit": max_results
        }

        if space_key:
            arguments["spaceKey"] = space_key

        return await self.call_tool("confluence_search", arguments)

    async def get_page(self, page_id: str) -> Dict[str, Any]:
        """Get page content by ID.

        Args:
            page_id: Confluence page ID

        Returns:
            Page content dictionary
        """
        return await self.call_tool("confluence_get_page", {"pageId": page_id})

    async def get_page_by_title(
        self,
        title: str,
        space_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get page by title.

        Args:
            title: Page title
            space_key: Optional space key

        Returns:
            Page content dictionary
        """
        arguments = {"title": title}
        if space_key:
            arguments["spaceKey"] = space_key

        return await self.call_tool("confluence_get_page_by_title", arguments)

    async def list_spaces(self) -> Dict[str, Any]:
        """List available Confluence spaces.

        Returns:
            List of spaces
        """
        return await self.call_tool("confluence_list_spaces", {})

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    def _generate_request_id(self) -> str:
        """Generate unique request ID."""
        import uuid
        return str(uuid.uuid4())


class MCPError(Exception):
    """Exception raised for MCP-specific errors."""
    pass


# Singleton instance for reuse
_mcp_client: Optional[ConfluenceMCPClient] = None


def get_mcp_client() -> ConfluenceMCPClient:
    """Get or create MCP client singleton.

    Returns:
        ConfluenceMCPClient instance
    """
    global _mcp_client

    if _mcp_client is None:
        _mcp_client = ConfluenceMCPClient()

    return _mcp_client
