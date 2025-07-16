from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import async_session
from app.db.models.message_schema import MessageCreate, MessageResponse, MessageUpdate
from app.crud.message_curd import (
    create_message, get_message, get_all_messages, update_message, delete_message
)

router = APIRouter(prefix="/messages", tags=["Messages"])

# Dependency
async def get_db():
    async with async_session() as session:
        yield session

@router.post("/", response_model=MessageResponse)
async def create(msg: MessageCreate, db: AsyncSession = Depends(get_db)):
    return await create_message(db, msg)

@router.get("/{message_id}", response_model=MessageResponse)
async def read(message_id: int, db: AsyncSession = Depends(get_db)):
    msg = await get_message(db, message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg

@router.get("/", response_model=List[MessageResponse])
async def read_all(db: AsyncSession = Depends(get_db)):
    return await get_all_messages(db)

@router.put("/{message_id}", response_model=MessageResponse)
async def update(message_id: int, msg: MessageUpdate, db: AsyncSession = Depends(get_db)):
    updated = await update_message(db, message_id, msg)
    if not updated:
        raise HTTPException(status_code=404, detail="Message not found")
    return updated

@router.delete("/{message_id}")
async def delete(message_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_message(db, message_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": "Message deleted"}
