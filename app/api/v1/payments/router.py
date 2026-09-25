from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import  select
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession


from api.v1.payments.schemas import CheckResponse, PaymentCreate, PaymentResponse
from api.v1.transactions.schemas import TransactionResponse, get_username
from models.users import User
from models.payments import Payment
from models.transactions import Transaction
from api.v1.users.router import get_user


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
    result = await db.scalars(payments)
    if result is None:
        raise HTTPException(status_code=404, detail="To'lov topilmadi")
                

    payments = result.all()
    return payments

@payments_router.post('/add/{user_id}')
async def create_paymment(user_id:int, payment: PaymentCreate, db = Depends(get_db)):

    current_user = await get_user(user_id, db)
    receiver = await get_user(payment.receiver_id, db)

    if current_user is None:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    if receiver is None:
        raise HTTPException(status_code=404, detail="Qabul qiluvchi topilmadi")
    print("4. Ikkala user ham mavjud")
    print("Sender balance:", current_user.balance)
    print("Payment amount:", payment.amount)

    if current_user.balance<payment.amount:
        raise HTTPException(status_code=404, detail="Balance yetarli emas")

    print("5. Transaction yaratilyapti")

    transaction = Transaction(
        user_id = user_id,
        amount = payment.amount,
        status = payment.status
    )
    print(transaction.status)
    db.add(transaction)
    await db.flush()

    print("6. Transaction ID:", transaction.id)

    payment = Payment(
        user_id = user_id,
        receiver_id = payment.receiver_id,
        transaction_id = transaction.id,
        amount = payment.amount,
        status = payment.status,
        created_at = payment.created_at
    )
    db.add(payment)

    current_user.balance -= payment.amount
    receiver.balance += payment.amount
    await db.commit()
    print("Transaction succes", transaction.id)
    return payment

@payments_router.patch("/balance/add/{user_id}", response_model=CheckResponse)
async def add_money(amount:float, user_id:int, db:AsyncSession = Depends(get_db)):
    user = select(User).where(User.id == user_id)
    result = await db.scalar(user)
    if result is None:
        raise HTTPException(status_code=404, detail="Bunday id li foydalanuvchi yo'q")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Iltimos, 0 dan katta son kiriting")

    transaction = Transaction(
        user_id = user_id,
        amount = amount,
        status = "completed"
    )
    db.add(transaction)
    await db.flush()
    result.balance += amount
    await db.commit()
    return CheckResponse(
        user_id = user_id,
        balance = result.balance,
        transaction_response = TransactionResponse(     
            id = transaction.id,
            user_id = transaction.user_id,
            user_name = await get_user(user_id, db),
            amount = transaction.amount,
            status = transaction.status,
            created_at = transaction.created_at
        )
    )


@payments_router.patch("/withdraw/{user_id}", response_model=CheckResponse)
async def withdraw_money(amount:float, user_id:int, db:AsyncSession = Depends(get_db)):
    user = select(User).where(User.id == user_id)
    result = await db.scalar(user)
    if result is None:
        raise HTTPException(status_code=404, detail="Bunday id li foydalanuvchi yo'q")
    if result.balance < amount:
        raise HTTPException(status_code=400, detail="Balance yetarli emas")
    transaction = Transaction(
        user_id = user_id,
        amount = amount,
        status = "completed"
    )
    db.add(transaction)
    await db.flush()
    result.balance -= amount
    await db.commit()
    return CheckResponse(
        user_id = user_id,
        balance = result.balance,
        transaction_response = TransactionResponse(
            id = transaction.id,
            user_id = transaction.user_id,
            user_name = await get_username(user_id, db),
            amount = transaction.amount,
            status = transaction.status,
            created_at = transaction.created_at
        )
    )