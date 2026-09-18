from enum import Enum
from decimal import Decimal
from datetime import datetime, timezone

from pydantic import BaseModel, Field, ConfigDict


class PaymentStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class PaymentBase(BaseModel):
    user_id: int
    amount: Decimal = Field(..., gt=0)


class PaymentCreate(PaymentBase):
    transaction_id: int
    receiver_id: int
    status: PaymentStatus
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

class PaymentResponse(PaymentBase):
    id: int
    transaction_id: int
    receiver_id: int
    status: PaymentStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)