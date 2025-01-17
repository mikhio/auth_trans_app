""" Модуль аутентификации"""

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db
from .logger import logger
from . import schemas, crud, models

from .env import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(
        data: dict,
        expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    """ Создание токена """

    logger.debug("create_access_token: %s", data)

    to_encode = data.copy()
    to_encode["sub"] = str(to_encode["sub"])

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})

    logger.debug("to_encode: %s", to_encode)

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)) -> models.User:
    """ Получение пользователя по токену """

    logger.debug("get_current_user")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Невалидный токен",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        logger.debug("Payload: %s", payload)

        user_id: int = int(payload.get("sub"))

        if user_id is None:
            logger.warning("Токен не содержит user_id в поле 'sub'")

            raise credentials_exception

        token_data = schemas.TokenData(user_id=user_id)
    except JWTError as e:
        logger.warning("Ошибка декодирования JWT: %s", e)

        raise credentials_exception from e

    user = await crud.get_user(db, user_id=token_data.user_id)
    logger.debug("user: %s", user)

    if user is None:
        logger.warning("Пользователь с id=%d не найден", token_data.user_id)

        raise credentials_exception

    return user
