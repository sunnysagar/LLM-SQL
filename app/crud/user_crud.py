from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import models
from app.db.models.user_schema import UserCreate, UserUpdate

User = models.User
Message = models.Message

async def create_user(db: AsyncSession, user: UserCreate):
    new_user = User(**user.dict())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

async def update_user(db: AsyncSession, user_id: int, user_data: UserUpdate):
    user = await get_user(db, user_id)
    if not user:
        return None
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)
    if not user:
        return None
    await db.delete(user)
    await db.commit()
    return user

async def get_messages_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(Message).where(Message.user_id == user_id))
    return result.scalars().all()