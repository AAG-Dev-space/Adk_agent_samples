# Confluence Documentation Assistant

A specialized AI agent for searching and understanding company Confluence documentation using the ADK (Agent Development Kit) and MCP (Model Context Protocol).

## 🎯 Features

### Multi-Agent Architecture
- **Query Analyzer**: Understands user intent and formulates search strategies
- **Document Searcher**: Searches Confluence via MCP tools
- **Answer Synthesizer**: Creates accurate, well-cited responses
- **Root Coordinator**: Orchestrates the entire workflow

### Core Capabilities
1. **Accurate Citations**: Always quotes exact text from Confluence with full source attribution
2. **Precise Search**: Uses MCP server to search company Confluence documentation
3. **Reasoning**: Multi-agent coordination for higher quality answers
4. **Source Transparency**: Every answer includes document titles, URLs, and last modified dates

## 🏗️ Architecture

```
User Question
     ↓
Root Coordinator
     ↓
     ├─→ Query Analyzer (analyzes intent)
     ├─→ Document Searcher (searches Confluence via MCP)
     └─→ Answer Synthesizer (creates cited response)
     ↓
Answer with Citations
```

### MCP Integration

This agent connects ONLY to your Confluence MCP server. It does NOT connect directly to Confluence.

```
Agent → MCP Server → Confluence
```

**MCP Server Requirements:**
- Your organization's Confluence MCP server must be running
- MCP server handles all Confluence authentication
- Agent only needs MCP server URL (and optional auth token)

## 🚀 Quick Start

### 1. Prerequisites

- Confluence MCP server running (e.g., http://mcp-server:3000)
- LiteLLM proxy (optional, for model management)
- Python 3.12+

### 2. Configuration

```bash
cp .env.example .env
```

Edit `.env`:

```bash
# Required: Your MCP server URL
CONFLUENCE_MCP_SERVER_URL=http://your-mcp-server:3000

# Optional: MCP server authentication
CONFLUENCE_MCP_API_TOKEN=your-token

# LLM Configuration
AGENT_MODEL=gemini/gemini-2.0-flash-exp
AGENT_API_BASE=http://localhost:4444
```

**IMPORTANT**: Confluence credentials (username, API token, base URL) are configured on the MCP server, NOT in this agent.

### 3. Run Locally

```bash
pip install -r requirements.txt
python server.py
```

The agent will start on port 8002 by default.

### 4. Run with Docker

```bash
docker build -t confluence-agent .
docker run -p 8002:8002 --env-file .env confluence-agent
```

### 5. Deploy to Agent Registry

```bash
# Build and push to Harbor
docker build -t harbor.company.com/agents/confluence-search:latest .
docker push harbor.company.com/agents/confluence-search:latest

# Deploy via Agent Registry UI:
# 1. Go to "Docker Images" page
# 2. Select confluence-search:latest
# 3. Configure environment variables
# 4. Click "Start"
```

## 📚 Usage Examples

### Example 1: Direct Question

**User**: "What is our authentication policy for API access?"

**Agent Response**:
```
## Answer
According to the Security Guidelines document, API authentication must use OAuth 2.0 with JWT tokens:

"All API endpoints must implement OAuth 2.0 authentication with short-lived JWT tokens (maximum 1 hour expiration). Refresh tokens should be rotated on each use."

- Source: [API Security Guidelines](https://confluence.company.com/display/SEC/API-Security)
- Last updated: 2024-11-15

## Sources
1. [API Security Guidelines](https://confluence.company.com/display/SEC/API-Security) - Last updated: 2024-11-15
   - Relevant excerpt: "All API endpoints must implement OAuth 2.0..."
```

### Example 2: Not Found

**User**: "What is the process for deploying to Mars?"

**Agent Response**:
```
I searched the Confluence documentation but could not find information about deploying to Mars.

I checked:
- Space: DEPLOY (deployment documentation)
- Search query: "Mars deployment"
- Recent pages in deployment space

Would you like me to search for general deployment processes instead?
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `CONFLUENCE_MCP_SERVER_URL` | MCP server URL | Yes | `http://localhost:3000` |
| `CONFLUENCE_MCP_API_TOKEN` | MCP auth token | No | `""` |
| `AGENT_MODEL` | LLM model | Yes | `gemini/gemini-2.0-flash-exp` |
| `AGENT_API_BASE` | LiteLLM proxy URL | No | - |
| `MAX_SEARCH_RESULTS` | Results per search | No | `5` |
| `CITATION_REQUIRED` | Force citations | No | `true` |
| `USE_REASONING` | Enable multi-agent | No | `true` |

### MCP Tools Available

The agent can use these MCP tools (provided by your MCP server):

- `search_confluence`: Full-text search
- `get_page_content`: Retrieve page by ID
- `search_in_space`: Search within specific space
- `list_recent_pages`: List recently updated pages
- `get_page_by_title`: Find page by exact title

## 🧪 Testing

Test the agent locally:

```python
import httpx

response = httpx.post(
    "http://localhost:8002/task/run",
    json={
        "contextId": "test-context",
        "taskId": "task-1",
        "task": {
            "message": "What is our coding standards for Python?"
        }
    }
)

print(response.json())
```

## 📊 AgentCard

The agent exposes an A2A AgentCard at:
```
http://localhost:8002/.well-known/agent-card.json
```

## 🔐 Security Notes

1. **No Direct Confluence Access**: This agent never connects to Confluence directly
2. **MCP Server Responsibility**: All Confluence credentials are on the MCP server
3. **Token Security**: Store MCP_API_TOKEN securely (use secrets management)
4. **Read-Only**: Agent only reads Confluence, never writes

## 📈 Performance

- **Multi-Agent Coordination**: Adds ~2-3 seconds overhead
- **Citation Quality**: Significantly improved accuracy
- **MCP Latency**: Depends on your MCP server response time

To reduce latency:
- Use `USE_REASONING=false` to disable multi-agent coordination
- Reduce `MAX_SEARCH_RESULTS`
- Use faster LLM models

## 🐛 Troubleshooting

### "MCP Client HTTP Error"

**Cause**: Cannot connect to MCP server

**Solution**:
1. Check MCP server is running: `curl http://your-mcp-server:3000/health`
2. Verify `CONFLUENCE_MCP_SERVER_URL` is correct
3. Check network connectivity

### "No results found" for known documents

**Cause**: MCP server search issues

**Solution**:
1. Test MCP server directly
2. Check Confluence credentials on MCP server
3. Verify Confluence space permissions

### Agent returns generic answers without citations

**Cause**: `CITATION_REQUIRED=false` or synthesis failure

**Solution**:
1. Set `CITATION_REQUIRED=true`
2. Check agent logs for errors
3. Ensure `USE_REASONING=true`

## 📖 References

- [ADK Documentation](https://github.com/google/adk-docs)
- [Multi-Agent Systems](https://github.com/google/adk-docs/blob/main/docs/agents/multi-agents.md)
- [MCP Integration](https://github.com/google/adk-docs/blob/main/docs/mcp/index.md)
- [A2A Protocol](https://github.com/google/adk-docs)


**Built with**:
- Google ADK (Agent Development Kit)
- A2A Protocol v0.3.0
- Model Context Protocol (MCP)
