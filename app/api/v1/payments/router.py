from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from typing import List


from api.v1.payments.schemas import PaymentResponse
from models.users import User
from models.payments import Payment


from db.base import get_db

payments_router = APIRouter(prefix="/payments",
                            tags=["Payments"]
                            )


@payments_router.get('/balance/{user_id}')
async def get_balance(user_id:int, db = Depends(get_db) ):
    balance = select(User.balance).where(user_id == User.id)
    result = await db.scalar(balance)
    if result is None:
        return HTTPException(status_code=404, detail="Bunday foydalanuvchi mavjud emas")


    return {f"{user_id} li user balanse":result}

@payments_router.get('/{user_id}', response_model=List[PaymentResponse])
async def get_payments(user_id:int, db = Depends(get_db)):
    payments = select(Payment).where(user_id == Payment.user_id)
    result = await db.scalar(payments)
    if result is None:
        raise HTTPException(status_code=404, detail="To'lov topilmadi")
                

    payments = result.all()
    return payments

@payments_router.post('/add/{user_id}')
async def create_paymment(user_id:int, db = Depends(get_db)):
    payment = Payment(
        user_id = user_id,
        
    )