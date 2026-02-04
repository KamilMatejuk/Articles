# similar to google/adk/models/gemma_llm.py

from typing_extensions import override
from google.adk.models.lite_llm import LiteLlm


class OllamaLLM(LiteLlm):
    """Generic Ollama-backed LLM for Google ADK via LiteLLM."""

    @classmethod
    @override
    def supported_models(cls) -> list[str]:
        return [r'ollama/.*']
