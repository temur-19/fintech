from pydantic import BaseModel, Decimal, Field

from datetime import datetime

class PaymentBase(BaseModel):
    user_id: int
    amount: Decimal = Field(..., gt=0)


class PaymentStatus(str):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class PaymentResponse(PaymentBase):
    id: int
    transaction_id: int
    status: PaymentStatus
    created_at: datetime

    class Config:
        orm_mode = True