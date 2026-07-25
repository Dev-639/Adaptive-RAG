"""
OpenAI LLM initialization and configuration.
"""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from src.core.config import settings

api_key = settings.OPENROUTER_API_KEY
base_url = settings.OPENROUTER_BASE_URL

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    openai_api_key=api_key,
    openai_api_base=base_url,
    max_tokens=1000,
)