from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import select


from models.users import User
from db.base import get_db
from schemas  import UserCreate




users_router = APIRouter(prefix='/users',
                   tags=['Users']
                   )


@users_router.get('/', summary='Get all users')
async def get_users(db:Session = Depends(get_db)):
    stmt = select(User)
    result = await db.scalars(stmt)
    users = result.all()
    return result

@users_router.post('/create/', tags=["Users"])
async def create_user(user_in:UserCreate, db:Session = Depends(get_db)):
    user = await db.scalars(select(User).where(User.first_name == user_in.first_name))
    if user:
        raise HTTPException(status_code=400, detail="Bunday ismli foydalanuvchi mavjud")
    user = UserCreate(first_name=user_in.first_name,
                      last_name=user_in.last_name,
                      )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

    