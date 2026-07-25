"""
Core configuration and environment settings.
Supports both .env files (local) and st.secrets (Streamlit Cloud).
"""

import os

from dotenv import load_dotenv

load_dotenv()


def _get_secret(key: str, default: str = "") -> str:
    """
    Get a secret from environment variables or Streamlit secrets.
    Prefers env vars, falls back to st.secrets for Streamlit Cloud.
    """
    val = os.getenv(key, "")
    if val:
        return val
    try:
        import streamlit as st
        return st.secrets.get(key, default)
    except Exception:
        return default


class Settings:
    """Application settings loaded from environment variables or Streamlit secrets."""

    OPENROUTER_API_KEY: str = _get_secret("OPENROUTER_API_KEY", _get_secret("OPENAI_API_KEY"))
    OPENAI_API_KEY: str = _get_secret("OPENROUTER_API_KEY", _get_secret("OPENAI_API_KEY"))
    OPENROUTER_BASE_URL: str = _get_secret("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    TAVILY_API_KEY: str = _get_secret("TAVILY_API_KEY")
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    CODE_COLLECTION = os.getenv("QDRANT_CODE_COLLECTION", "codebase")
    DOCS_COLLECTION = os.getenv("QDRANT_DOCS_COLLECTION", "guidelines")


settings = Settings()

# Set env variables for LangChain & OpenAI/OpenRouter integrations
os.environ["OPENROUTER_API_KEY"] = settings.OPENROUTER_API_KEY
os.environ["OPENAI_API_KEY"] = settings.OPENROUTER_API_KEY
os.environ["OPENAI_API_BASE"] = settings.OPENROUTER_BASE_URL
os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY
