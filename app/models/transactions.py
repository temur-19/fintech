from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, MappedColumn, relationship, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Enum

from db.base import Base
from app.models.users import User

class Transaction(Base):
    __tablename__ = "transactions"
    id = MappedColumn(Integer, primary_key=True, index=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    amount = MappedColumn(Integer, nullable=False)
    status = MappedColumn(Enum("pending", "completed", "failed", name="transaction_status"), nullable=False)

