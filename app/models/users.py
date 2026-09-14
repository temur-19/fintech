from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import MappedColumn, relationship
from sqlalchemy.ext.declarative import declarative_base
import random

from db.base import Base



def generate_card_number() -> str:
    return ''.join(str(random.randint(1000, 9999)) for _ in range(4))
    
class User(Base):
    __tablename__ = "users"
    id = MappedColumn(Integer, primary_key=True, index=True)
    first_name = MappedColumn(String, nullable = False)
    last_name = MappedColumn(String, nullable = False)
    card_number = MappedColumn(String, nullable = False, unique=True, default=generate_card_number)
    balance = MappedColumn(Integer, nullable = False, default=0)

