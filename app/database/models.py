from sqlalchemy import BigInteger, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

import os
from dotenv import load_dotenv


load_dotenv()

engine = create_async_engine(os.getenv("DATABASE_URL"))

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True , nullable=False)
    tg_id = mapped_column(BigInteger , nullable=False)


class Shop(Base):
    __tablename__ = "shops"

    id: Mapped[int] = mapped_column(primary_key=True , nullable=False)
    tg_id = mapped_column(BigInteger , nullable=False)
    api_key: Mapped[str] = mapped_column(Text , nullable=False)
    shop_name: Mapped[str] = mapped_column(String(100))
    
    
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)