"""
    This file handles:

Sending your query (with FAISS context) to a selected LLM

Returning the generated reply

Supporting multiple LLM providers (via config)
"""


from app.config import settings
from openai import OpenAI
from anthropic import Anthropic   # for claude

# Clients
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
claude_client = Anthropic(api_key=settings.CLAUDE_API_KEY)

# Claude
async def query_claude(prompt: str) -> str:
    try:
        response = claude_client.messages.create(
            model="claude-3-opus-20240229",  # Or use 'claude-3-sonnet-20240229' for cheaper model
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

async def query_grok(prompt: str) -> str:
    # Replace with real Grok API integration
    return f"[Grok] {prompt}"

# client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def query_openai(prompt: str) -> str:
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4.1",  # Or "gpt-4"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI API error: {str(e)}"
    
async def get_llm_response(prompt: str, provider: str = "openai") -> str:
    """
    Chooses LLM provider based on settings
    """
    provider = provider.lower()

    if provider == "openai":
        return await query_openai(prompt)
    elif provider == "claude":
        return await query_claude(prompt)
    elif provider == "grok":
        return await query_grok(prompt)
    else:
        return "LLM provider not supported."
