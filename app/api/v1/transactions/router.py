from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from db.base import get_db
from models.transactions import Transaction
from api.v1.transactions.schemas import TransactionResponse


transactions_router = APIRouter(prefix =  "/transactions",
                       tags = ["transactions"])


@transactions_router.get('/get/{user_id}', response_model=List[TransactionResponse])
async def get_transactions(user_id:int, db:AsyncSession = Depends(get_db)):
    stmt = Select(Transaction).where(Transaction.user_id == user_id)
    transactions = await db.scalars(stmt)
    if stmt is None:
        raise HTTPException(status_code=404, detail="Tranzaksiyalar topilmadi")
    result = transactions.all()
    return result