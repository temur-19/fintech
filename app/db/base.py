from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from dotenv import load_dotenv
import os


load_dotenv()

ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL") or os.getenv("DATABASE_URL")

if not ASYNC_DATABASE_URL:
    raise ValueError("ASYNC_DATABASE_URL or DATABASE_URL is not set")

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
)

Session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with Session() as session:
        yield session


get_async_session = get_db
