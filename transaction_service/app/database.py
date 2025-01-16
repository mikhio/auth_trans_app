# transaction_service/app/database.py

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .env import DATABASE_URL
from .logger import logger

logger.info("Создание async engine по URL: %s", DATABASE_URL)

async_engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Генератор сессии для зависимостей"""
    async with AsyncSessionLocal() as session:
        yield session
