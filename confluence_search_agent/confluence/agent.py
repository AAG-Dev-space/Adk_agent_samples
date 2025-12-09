"""Confluence Search Agent - Multi-Agent System with MCP Integration

This agent uses a hierarchical multi-agent structure:
- Root Coordinator: Orchestrates the overall search and response flow
- Query Analyzer: Analyzes user intent and formulates search strategy
- Document Searcher: Searches Confluence via MCP tools
- Answer Synthesizer: Creates accurate, cited responses

MCP Integration:
- Uses ADK's official McpToolset with streamable-http (SSE) connection
- Dynamically discovers tools from the MCP server at runtime
- All Confluence credentials are managed by the MCP server

References:
- Multi-Agent Systems: https://github.com/google/adk-docs/blob/main/docs/agents/multi-agents.md
- MCP Integration: https://google.github.io/adk-docs/tools-custom/mcp-tools/
"""

from google.adk.agents import LlmAgent

from .config import llm_model, confluence_mcp_toolset
from .prompt import (
    root_coordinator_instruction,
    query_analyzer_instruction,
    document_searcher_instruction,
    answer_synthesizer_instruction
)

# Sub-Agent 1: Query Analyzer
# Analyzes user questions and formulates search strategy
query_analyzer = LlmAgent(
    model=llm_model,
    name="query_analyzer",
    description="Analyzes user questions to extract search intent, keywords, and strategy",
    instruction=query_analyzer_instruction,
    tools=[]  # Pure reasoning agent, no tools needed
)

# Sub-Agent 2: Document Searcher
# Executes searches and retrieves Confluence content via MCP
# Uses McpToolset which dynamically discovers tools from the MCP server
document_searcher = LlmAgent(
    model=llm_model,
    name="document_searcher",
    description="Searches Confluence documentation using MCP tools and retrieves relevant pages",
    instruction=document_searcher_instruction,
    tools=[confluence_mcp_toolset]  # ADK's official MCP integration
)

# Sub-Agent 3: Answer Synthesizer
# Creates accurate, well-cited responses from retrieved documents
answer_synthesizer = LlmAgent(
    model=llm_model,
    name="answer_synthesizer",
    description="Synthesizes accurate answers with proper citations from Confluence documents",
    instruction=answer_synthesizer_instruction,
    tools=[]  # Synthesis and reasoning only
)

# Root Agent: Coordinator
# Orchestrates the multi-agent workflow
root_agent = LlmAgent(
    model=llm_model,
    name="confluence_documentation_assistant",
    description="Expert assistant for searching and understanding company Confluence documentation. "
                "Provides accurate, well-cited answers by coordinating specialized sub-agents. "
                "Always cites sources and quotes exact text from documents.",
    instruction=root_coordinator_instruction,
    sub_agents=[
        query_analyzer,
        document_searcher,
        answer_synthesizer
    ]
)
