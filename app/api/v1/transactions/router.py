from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from app.db.base import get_db
from app.models.transactions import Transaction
from app.api.v1.transactions.schemas import TransactionResponse
from app.api.v1.transactions.schemas import get_username


transactions_router = APIRouter(prefix =  "/transactions",
                       tags = ["transactions"])


@transactions_router.get('/get/{user_id}', response_model=List[TransactionResponse])
async def get_transactions(user_id:int, db:AsyncSession = Depends(get_db)):
    stmt = Select(Transaction).where(Transaction.user_id == user_id)
    transactions = await db.scalars(stmt)
    result = transactions.all()
    if result is None:
            raise HTTPException(status_code=404, detail="Tranzaksiyalar topilmadi")
    response = []
    for i in result:
        userfullname = await get_username(i.user_id,db)
        response.append(TransactionResponse(
            id=i.id,
            user_id=i.user_id,
            user_name=userfullname,
            amount=i.amount,
            status=i.status,
            created_at=i.created_at
            ))


    return response