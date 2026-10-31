"""
App Settings
============

Shared runtime objects for the platform.

Set OLLAMA_HOST (e.g. http://host.docker.internal:11434) to use a local Ollama model; OLLAMA_MODEL selects it.
Otherwise set GOOGLE_API_KEY to use Gemini instead of OpenAI. GEMINI_MODEL selects the chat model.
"""

from os import getenv

from agno.models.base import Model
from agno.models.openai import OpenAIResponses


def _model() -> Model:
    if getenv("OLLAMA_HOST"):
        from agno.models.ollama import Ollama

        return Ollama(id=getenv("OLLAMA_MODEL", "qwen2.5:3b"), host=getenv("OLLAMA_HOST"))
    if getenv("GOOGLE_API_KEY"):
        from agno.models.google import Gemini

        return Gemini(id=getenv("GEMINI_MODEL", "gemini-3.5-flash"))
    return OpenAIResponses(id="gpt-6.1-sol")


def fallback_models() -> list[Model]:
    """Models tried in order when the primary model errors or is rate limited.

    With GOOGLE_API_KEY set, Gemini Flash-Lite goes first (free-tier quotas are counted per model).
    Set OLLAMA_FALLBACK_HOST (e.g. http://host.docker.internal:11434) to end the chain with a local Ollama model.
    """
    models: list[Model] = []
    if getenv("GOOGLE_API_KEY") and not getenv("OLLAMA_HOST"):
        from agno.models.google import Gemini

        models.append(Gemini(id=getenv("GEMINI_FALLBACK_MODEL", "gemini-3.5-flash-lite")))
    host = getenv("OLLAMA_FALLBACK_HOST")
    if host:
        from agno.models.ollama import Ollama

        models.append(Ollama(id=getenv("OLLAMA_FALLBACK_MODEL", "qwen2.5:3b"), host=host))
    return models


def default_model() -> Model:
    """Fresh model instance per agent — avoids shared-state footguns."""
    return _model()


def manager_model() -> Model:
    """Model for OS Manager and Company Product Manager."""
    return _model()
