from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text
from core.config import settings

engine = create_engine(

    url=settings.DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=15,
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=15,
)

session_fabrik = sessionmaker(engine)
async_session = async_sessionmaker(async_engine)

async_engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_db():
    async with AsyncSessionLocal() as session:  # ✅ правильно
        yield session

class Base(DeclarativeBase):
    pass