# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from google.adk.models.lite_llm import LiteLlm

# Get model configuration from environment variables
AGENT_MODEL = os.getenv("AGENT_MODEL", "gemini/gemini-2.5-flash")
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
