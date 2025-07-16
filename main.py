"""
    This file:

Starts the FastAPI app

Loads documents into FAISS when the app starts

Registers the /chat route
"""

from fastapi import FastAPI
from app.routes import chat_route, user_route, message_route
from app.services.faiss_service import load_documents
import asyncio
from app.db.database import engine, Base

app = FastAPI(title="LLM Chat API")

# Register routes
app.include_router(chat_route.router, prefix="/llm", tags=["LLM"])
app.include_router(user_route.router, prefix="/user", tags=["Users"])
app.include_router(message_route.router, prefix="/message", tags=["Messages"])

# from openai import OpenAI
# client = OpenAI()

# response = client.responses.create(
#     model="gpt-4.1",
#     input="Write a one-sentence bedtime story about a unicorn."
# )

# print(response.output_text)


@app.on_event("startup")
async def on_startup():
    # Load documents from file into FAISS
    await asyncio.sleep(1)
    try:
        with open("data/docs.txt", "r", encoding="utf-8") as f:
            docs = [line.strip() for line in f.readlines() if line.strip()]
        load_documents(docs)
        print(f"✅ Loaded {len(docs)} documents into FAISS.")
    except FileNotFoundError:
        print("❌ 'data/docs.txt' not found. Please add some documents.")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created.")
