""" Модуль для работы с Auth сервисом """

import httpx

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from . import schemas
from .logger import logger
from .env import AUTH_SERVICE_URL


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def valid_token( token: str = Depends(oauth2_scheme)) -> schemas.User:
    """Запрос к Auth сервису для верификации токена """

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{AUTH_SERVICE_URL}/verify", json={}, headers=headers)
            response.raise_for_status()

            return schemas.User(
                uid=response.json().get("id"),
                username=response.json().get("username"))

        except httpx.HTTPStatusError as e:
            logger.error("Не удалось войти по токену: %s", token)
            logger.error("HTTPStatusError: %s", e)

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден") from e


async def fetch_user(username: str) -> int:
    """Запрос к Auth сервису для получения информации о пользователе """

    headers = {
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/check-user",
                json={"username": username},
                headers=headers)

            response.raise_for_status()

            return response.json().get("id")
        except httpx.HTTPStatusError as e:
            logger.error("Не удалось найти пользователя %s", username)
            logger.error("HTTPStatusError: %s", e)

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден") from e
