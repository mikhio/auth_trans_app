""" Модуль аунтетификации"""

from typing import Generator
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from .database import SessionLocal
from .logger import logger
from . import schemas, crud, models

from .env import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(
        data: dict,
        expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    """ Создание токена """

    to_encode = data.copy()
    to_encode["sub"] = str(to_encode["sub"])

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})

    logger.info(to_encode)

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def get_db() -> Generator[Session, None, None]:
    """ Генератор сессии для зависимостей """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)) -> models.User:
    """ Получение пользователя по токену """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Невалидный токен",
        headers={"WWW-Authenticate": "Bearer"},
    )

    logger.info("Получил token %s", token)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info("Pyload sub: %s", payload.get("sub")) 
        user_id: int = int(payload.get("sub"))

        if user_id is None:
            logger.warning("Токен не содержит user_id в поле 'sub'")
            raise credentials_exception

        token_data = schemas.TokenData(user_id=user_id)
    except JWTError as e:
        logger.warning("Ошибка декодирования JWT: %s", e)
        raise credentials_exception from e

    user = crud.get_user(db, user_id=token_data.user_id)

    if user is None:
        logger.warning("Пользователь с id=%d не найден", token_data.user_id)
        raise credentials_exception

    return user
