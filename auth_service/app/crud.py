""" Модуль CRUD """

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

from . import models, schemas
from .logger import logger


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_username(db: AsyncSession, username: str) -> models.User | None:
    """ Возвращает пользователя по username """

    logger.debug("get_user_by_username: %s", username)

    result = await db.execute(select(models.User).where(models.User.username == username))

    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str) -> models.User | None:
    """ Возвращает пользователя по email """

    logger.debug("get_user_by_email: %s", email)

    result = await db.execute(select(models.User).where(models.User.email == email))

    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    """ Создает пользователя """

    logger.debug("create_user: %s", user.username)

    hashed_password = pwd_context.hash(user.password)

    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password)

    db.add(db_user)

    await db.commit()
    await db.refresh(db_user)

    return db_user

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Проверяет пароль """

    logger.debug("verify_password")

    return pwd_context.verify(plain_password, hashed_password)

async def get_user(db: AsyncSession, user_id: int) -> models.User | None:
    """ Возвращает пользователя по user_id"""

    logger.debug("get_user: %d", user_id)

    result = await db.execute(select(models.User).where(models.User.id == user_id))

    return result.scalars().first()

async def update_password(db: AsyncSession, user: models.User, new_password: str) -> models.User:
    """ Обновляет пароль """
    
    logger.debug("update_password: %s", user)

    user.hashed_password = pwd_context.hash(new_password)

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return user
