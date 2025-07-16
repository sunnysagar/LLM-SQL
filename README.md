# LLM-SQL APP

## 🔹 Task 1: /chat Endpoint with LLM Integration
- Accepts a user query
- Performs FAISS vector search for context
- Supports multiple LLM providers: OpenAI, Claude, Grok
- LLM provider is configurable

## 🔹 Task 2: Full CRUD with Async SQLAlchemy
- Models: User, Message
- Async database session using SQLite
- FastAPI endpoints with full CRUD for both
- Includes message listing by user

## 🔧 Run Instructions

1. Install dependencies:
    pip install -r requirements.txt

2. Run the app:
    uvicorn app.main:app --reload

3. Visit: http://localhost:8000/docs