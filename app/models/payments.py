from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, MappedColumn, relationship, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Enum

from db.base import Base


class Payment(Base):
    __tablename__ = "payments"
    id = MappedColumn(Integer, primary_key=True, index=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    transaction_id:Mapped[int] = mapped_column(Integer, ForeignKey("transactions.id"), nullable =False)
    amount = MappedColumn(Integer, nullable=False)
    status = MappedColumn(Enum("pending", "completed", "failed", name="payment_status"), nullable=False)
    created_at = MappedColumn(String, nullable=False)
