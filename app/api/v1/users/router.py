from fastapi import APIRouter, Depends, HTTPException
from fastapi import security
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, select
from typing import List

from api.v1.users.schemas import UserCreate, UserListResponse, UserResponse
from api.v1.transactions.schemas import UserResponse
from db.base import Session, get_db
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


@users_router.get('/{user_id}')
async def get_user(user_id:int, db:AsyncSession = Depends(get_db)):
    user = Select(User).where(User.id == user_id)
    result = await db.scalar(user)
    if result is None:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    return result

@users_router.post('/create/', tags=["Users"])
async def create_user(user_in:UserCreate, db:AsyncSession = Depends(get_db)):
    user = User(first_name=user_in.first_name,
                      last_name=user_in.last_name,
                      )
    db.add(user)
    await db.commit()
    await db.refresh(user)      
    return user

@users_router.post('/login/', response_model=UserResponse, tags=["Users"])
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.username == form.username))
    if not user:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud emas")

    if not security.verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Username yoki parol noto'g'ri")

    access_token = security.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

