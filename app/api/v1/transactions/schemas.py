from decimal import Decimal
from datetime import datetime, timezone

from pydantic import BaseModel, Field
from enum import Enum

class TransactionStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class TransactionResponse(BaseModel):
    id: int | None = None
    user_id: int
    amount: Decimal
    status: TransactionStatus
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

