"""
This file handles:

- Sending a user query (with FAISS context) to a selected LLM
- Returning the generated reply
- Supporting multiple LLM providers (OpenAI, Claude, Grok)
"""

from app.config import settings
from openai import OpenAI
from anthropic import Anthropic
import httpx

# === Clients ===
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
claude_client = Anthropic(api_key=settings.CLAUDE_API_KEY)

# === Claude Integration ===
async def query_claude(prompt: str) -> str:
    try:
        response = claude_client.messages.create(
            model="claude-3-opus-20240229",  # Or claude-3-sonnet-20240229 for a cheaper model
            max_tokens=500,
            temperature=0.7,
            system="You are a helpful assistant.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        return f"Claude API error: {str(e)}"

# === Grok Integration (Placeholder, future-ready) ===
async def query_grok(prompt: str) -> str:
    """
    Async function to call Grok LLM API.
    Replace with actual endpoint and logic once Grok API is publicly available.
    """
    GROK_API_KEY = settings.GROK_API_KEY
    GROK_ENDPOINT = "https://api.grok.ai/v1/chat/completions"  # Hypothetical

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-3-latest",  # Replace with real model name when known
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(GROK_ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        return f"Grok API error: HTTP {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Grok API error: {str(e)}"

# === OpenAI Integration ===
async def query_openai(prompt: str) -> str:
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4.1",  # Use "gpt-4" or "gpt-3.5-turbo" as fallback if needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI API error: {str(e)}"

# === Main LLM Selector ===
async def get_llm_response(prompt: str, provider: str = "openai") -> str:
    """
    Dynamically selects and queries the chosen LLM provider.
    """
    provider = provider.lower()

    if provider == "openai":
        return await query_openai(prompt)
    elif provider == "claude":
        return await query_claude(prompt)
    elif provider == "grok":
        return await query_grok(prompt)
    else:
        return "LLM provider not supported. Please choose openai, claude, or grok."
