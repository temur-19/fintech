from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Enum


class TransactionStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class TransactionResponse(BaseModel):
    id: int | None = None
    user_id: int
    amount: Decimal
    status: TransactionStatus
    created_at: datetime

