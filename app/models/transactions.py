from sqlalchemy import Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, MappedColumn, mapped_column

from db.base import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id = MappedColumn(Integer, primary_key=True, index=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    amount = MappedColumn(Integer, nullable=False)
    status = MappedColumn(Enum("pending", "completed", "failed", name="transaction_status"), nullable=False)

