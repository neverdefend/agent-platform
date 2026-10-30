"""
App Settings
============

Shared runtime objects for the platform.

Set GOOGLE_API_KEY to use Gemini instead of OpenAI. GEMINI_MODEL selects the chat model.
"""

from os import getenv

from agno.models.base import Model
from agno.models.openai import OpenAIResponses


def _model() -> Model:
    if getenv("GOOGLE_API_KEY"):
        from agno.models.google import Gemini

        return Gemini(id=getenv("GEMINI_MODEL", "gemini-3.5-flash"))
    return OpenAIResponses(id="gpt-6.1-sol")


def default_model() -> Model:
    """Fresh model instance per agent — avoids shared-state footguns."""
    return _model()


def manager_model() -> Model:
    """Model for OS Manager and Company Product Manager."""
    return _model()
