import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, MappedColumn, mapped_column
from datetime import datetime

from app.db.base import Base


class Payment(Base):
    __tablename__ = "payments"
    id = MappedColumn(Integer, primary_key=True, index=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    transaction_id:Mapped[int] = mapped_column(Integer, ForeignKey("transactions.id"), nullable =False)
    amount = MappedColumn(Integer, nullable=False)
    status = MappedColumn(Enum("pending", "completed", "failed", name="payment_status"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    nullable=False
)
