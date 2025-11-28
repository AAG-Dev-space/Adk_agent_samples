# Personalized Shopping Agent - A2A Exposed

ADK Personalized Shopping Agent exposed via A2A Protocol using `to_a2a()`.

## Features

- ✅ **A2A Protocol v0.3.0** via ADK's `to_a2a()`
- ✅ **Auto-generated AgentCard** at `/.well-known/agent-card.json`
- ✅ **Auto-extracted Skills** from agent tools
- ✅ **Docker Ready**
- ✅ **Single Command Deploy**

## Quick Start

### Build & Run

```bash
# Build image
cd test_agent_server
docker build -t personalized-shopping:v1.0.0 .

# Run container
docker run -d \
  -p 8000:8000 \
  --name shopping-agent \
  -e GOOGLE_CLOUD_PROJECT=your-project-id \
  personalized-shopping:v1.0.0

# Check AgentCard (auto-generated)
curl http://localhost:8000/.well-known/agent-card.json

# Check health
curl http://localhost:8000/health || curl http://localhost:8000/.well-known/agent-card.json
```

### Push to Private Registry

```bash
# Tag for registry
docker tag personalized-shopping:v1.0.0 localhost:5000/personalized-shopping:v1.0.0

# Push
docker push localhost:5000/personalized-shopping:v1.0.0

# Verify in registry
curl http://localhost:5000/v2/_catalog
curl http://localhost:5000/v2/personalized-shopping/tags/list
```

## How It Works

### ADK's `to_a2a()` Function

The `to_a2a()` utility automatically:

1. **Generates AgentCard** from agent metadata and tools
2. **Exposes A2A endpoints** for agent-to-agent communication
3. **Extracts skills** from FunctionTools (search, click)
4. **Serves at** `/.well-known/agent-card.json`

### server.py

```python
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from personalized_shopping.agent import root_agent

# One-line A2A exposure
a2a_app = to_a2a(root_agent, port=8000)
```

### Auto-Generated AgentCard

The AgentCard includes:

- **Name**: `personalized_shopping_agent`
- **Skills**: Extracted from `search()` and `click()` tools
- **Capabilities**: Auto-detected from agent configuration
- **Protocol Version**: A2A v0.3.0
- **Input/Output Modes**: text/plain

## Environment Variables

Required:

- `GOOGLE_CLOUD_PROJECT` - Your GCP project ID (for Gemini API)

Optional:

- `GOOGLE_CLOUD_REGION` - GCP region (default: us-central1)
- `PORT` - Server port (default: 8000)

## Testing A2A Endpoints

### 1. Get AgentCard

```bash
curl http://localhost:8000/.well-known/agent-card.json | jq .
```

### 2. Chat via A2A Protocol

```bash
# Test chat (protocol details handled by to_a2a)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I want a summer dress"}'
```

## Deploying to Agent Registry

Once pushed to `localhost:5000`, the Agent Registry can:

1. Pull the image: `docker pull localhost:5000/personalized-shopping:v1.0.0`
2. Run on port 8100-8199
3. Fetch AgentCard from `http://localhost:8100/.well-known/agent-card.json`
4. Display in agent list with auto-extracted skills

## Architecture

```
┌─────────────────────────────────────┐
│  to_a2a() Wrapper                  │
│  - Auto AgentCard generation       │
│  - A2A protocol endpoints          │
│  - Skill extraction from tools     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  ADK Personalized Shopping Agent   │
│  - FunctionTool(search)            │
│  - FunctionTool(click)             │
│  - Gemini 2.5 Flash model          │
└─────────────────────────────────────┘
```

## Notes

- No manual AgentCard JSON needed (`to_a2a` generates it)
- Skills auto-extracted from agent's tools
- First run may take time to load product data
- Session management handled by ADK
