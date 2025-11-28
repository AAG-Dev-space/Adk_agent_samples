"""
A2A-compliant server for Personalized Shopping Agent using ADK's to_a2a()
"""
import sys
import os
from pathlib import Path

# Add personalized_shopping to Python path
sys.path.insert(0, str(Path(__file__).parent))

from google.adk.a2a.utils.agent_to_a2a import to_a2a
from personalized_shopping.agent import root_agent

# Get configuration from environment variables
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "localhost")
PROTOCOL = os.getenv("PROTOCOL", "http")

# Convert ADK agent to A2A-compatible application
# This automatically:
# - Generates AgentCard from agent metadata
# - Exposes AgentCard at /.well-known/agent-card.json
# - Provides A2A protocol endpoints
# - Extracts skills from agent tools
# Note: The AgentCard URL will be constructed as {protocol}://{host}:{port}
a2a_app = to_a2a(
    root_agent,
    host=HOST,
    port=PORT,
    protocol=PROTOCOL,
    # AgentCard will be auto-generated from agent metadata
)

# The application is now ready to be served with uvicorn
# uvicorn server:a2a_app --host 0.0.0.0 --port 8000
