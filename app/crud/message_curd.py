from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Message
from app.schemas.message_schema import MessageCreate, MessageUpdate

async def create_message(db: AsyncSession, message: MessageCreate):
    new_message = Message(**message.dict())
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    return new_message

async def get_message(db: AsyncSession, message_id: int):
    result = await db.execute(select(Message).where(Message.id == message_id))
    return result.scalar_one_or_none()

async def get_all_messages(db: AsyncSession):
    result = await db.execute(select(Message))
    return result.scalars().all()

async def update_message(db: AsyncSession, message_id: int, data: MessageUpdate):
    message = await get_message(db, message_id)
    if not message:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(message, key, value)
    await db.commit()
    await db.refresh(message)
    return message

async def delete_message(db: AsyncSession, message_id: int):
    message = await get_message(db, message_id)
    if not message:
        return None
    await db.delete(message)
    await db.commit()
    return message
