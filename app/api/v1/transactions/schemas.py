from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from fastapi import Depends


from pydantic import BaseModel, Field
from enum import Enum
from app.models.users import User
class TransactionStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


async def get_username(user_id:int, db:AsyncSession = Depends(get_db)):
    stmt = select(User.first_name, User.last_name).where(User.id == user_id)
    fullname = await db.execute(stmt)
    user = fullname.one_or_none()
    if user is None:
        return None
    return {
        "first_name":user.first_name,
        "last_name":user.last_name
    }



class UserResponse(BaseModel):
    first_name:str
    last_name:str
class TransactionResponse(BaseModel):
    id: int | None = None
    user_id: int
    user_name:UserResponse
    amount: Decimal
    status: TransactionStatus
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

