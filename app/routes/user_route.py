"""
User API routes for CRUD operations and message retrieval.
Endpoints:
- POST /: Create a new user.
- GET /{user_id}: Retrieve a user by ID.
- GET /: Retrieve all users.
- PUT /{user_id}: Update a user by ID.
- DELETE /{user_id}: Delete a user by ID.
- GET /{user_id}/messages: Retrieve messages for a user.
Dependencies:
- Uses FastAPI, SQLAlchemy AsyncSession, and custom CRUD/user/message schemas.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import async_session
from app.db.models.user_schema import UserCreate, UserResponse, UserUpdate
from app.db.models.message_schema import MessageResponse
from app.crud.user_crud import create_user, get_user, get_all_users, update_user, delete_user, get_messages_by_user

router = APIRouter()

async def get_db():
    async with async_session() as session:
        yield session

@router.post("/", response_model=UserResponse)
async def create(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)

@router.get("/{user_id}", response_model=UserResponse)
async def read(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserResponse])
async def read_all(db: AsyncSession = Depends(get_db)):
    return await get_all_users(db)

@router.put("/{user_id}", response_model=UserResponse)
async def update(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    updated = await update_user(db, user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/{user_id}")
async def delete(user_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

@router.get("/{user_id}/messages", response_model=List[MessageResponse])
async def get_user_messages(user_id: int, db: AsyncSession = Depends(get_db)):
    messages = await get_messages_by_user(db, user_id)
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for this user")
    return messages
