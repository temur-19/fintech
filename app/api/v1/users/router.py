from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from api.v1.users.schemas import UserCreate, UserListResponse
from db.base import get_db
from models.users import User




users_router = APIRouter(prefix='/users',
                   tags=['Users']
                   )


@users_router.get('/', response_model = UserListResponse)
async def get_users(db:AsyncSession = Depends(get_db)):
    stmt = select(User)
    result = await db.scalars(stmt)
    users = result.all()
    return {"users":users}

@users_router.post('/create/', tags=["Users"])
async def create_user(user_in:UserCreate, db:AsyncSession = Depends(get_db)):
    user = User(first_name=user_in.first_name,
                      last_name=user_in.last_name,
                      )
    db.add(user)
    await db.commit()
    await db.refresh(user)      
    return user

    