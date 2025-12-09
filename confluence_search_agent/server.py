"""A2A Server for Confluence Search Agent"""
import os
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from confluence.agent import root_agent

# A2A Server configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8002"))
PROTOCOL = os.getenv("PROTOCOL", "JSONRPC")  # JSONRPC or REST

# Convert ADK agent to A2A-compatible FastAPI app
app = to_a2a(
    root_agent,
    host=HOST,
    port=PORT,
    protocol=PROTOCOL,
)

if __name__ == "__main__":
    import uvicorn

    print(f"📚 Starting Confluence Documentation Assistant on {HOST}:{PORT}")
    print(f"📋 Protocol: {PROTOCOL}")
    print(f"🔍 Multi-Agent System: Query Analyzer → Document Searcher → Answer Synthesizer")
    print(f"🌐 AgentCard URL: http://{HOST if HOST != '0.0.0.0' else 'localhost'}:{PORT}/.well-known/agent-card.json")

    uvicorn.run(app, host=HOST, port=PORT)
