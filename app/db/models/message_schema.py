"""
This script will handle teh message schema for crud opr
"""

from pydantic import BaseModel
from typing import Optional

class MessageCreate(BaseModel):
    content: str
    user_id: int  # Link to the user

class MessageUpdate(BaseModel):
    content: Optional[str] = None

class MessageResponse(BaseModel):
    id: int
    content: str
    user_id: int

    class Config:
        orm_mode = True
