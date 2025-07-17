"""
    This file handles:

Reading environment variables (like your LLM provider or API keys)

Centralizing all configuration for easy control

"""

# app/config.py
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Settings class to access env values
class Settings:
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # default: openai

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")  # Optional
    GROK_API_KEY = os.getenv("GROK_API_KEY")      # Optional

settings = Settings()
