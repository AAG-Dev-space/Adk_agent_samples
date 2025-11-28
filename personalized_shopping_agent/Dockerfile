FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy project files
COPY pyproject.toml uv.lock* ./
COPY README.md ./
COPY personalized_shopping/ ./personalized_shopping/
COPY server.py ./

# Install dependencies (including a2a extras and litellm)
RUN uv pip install --system "google-adk[a2a]" "litellm>=1.0.0" && \
    uv sync --no-dev

# Create data directory for products
RUN mkdir -p personalized_shopping/shared_libraries/data
RUN mkdir -p personalized_shopping/shared_libraries/search_engine/indexes

# Expose port
EXPOSE 8000

# Set environment variables
ENV PORT=8000
ENV HOST="localhost"
ENV PROTOCOL="http"
ENV PYTHONUNBUFFERED=1

# Agent configuration (can be overridden at runtime)
ENV AGENT_MODEL="gemini-2.5-flash"
ENV AGENT_API_BASE=""
ENV AGENT_API_KEY=""

# Health check (AgentCard endpoint)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/.well-known/agent-card.json || exit 1

# Run server using uvicorn
CMD ["uvicorn", "server:a2a_app", "--host", "0.0.0.0", "--port", "8000"]
