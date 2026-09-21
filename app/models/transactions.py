from sqlalchemy import Enum, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, MappedColumn, mapped_column
from datetime import datetime, timezone

from db.base import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id = MappedColumn(Integer, primary_key=True, index=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    amount = MappedColumn(Integer, nullable=False)
    status = MappedColumn(Enum("pending", "completed", "failed", name="transaction_status"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc),
    nullable=False
)
