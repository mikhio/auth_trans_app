""" Микросервис аутентификации """

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas, crud, auth
from .database import get_db
from .logger import logger


app = FastAPI(title="Auth Microservice")

@app.post("/register", response_model=schemas.UserOut)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)) -> models.User:
    """ Регистрация пользователя """

    logger.debug("register: %s", user.username)
    logger.info("Попытка зарегистрироваться: %s", user.username)

    db_user = await crud.get_user_by_username(db, username=user.username)

    if db_user:
        logger.warning(
            "Регистрация неудачна: пользователь %s уже существует",
            db_user.username)

        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    db_user = await crud.create_user(db, user)
    logger.info("Пользователь зарегистрирован: %s", db_user.username)

    return db_user

@app.post("/check-user", response_model=schemas.UserFound)
async def check_user(user: schemas.Username, db: AsyncSession = Depends(get_db)) -> models.User:
    """ Проверка регистрации пользователя """

    logger.debug("check_user: %s", user.username)
    logger.info("Поиск пользователя %s для проверки", user.username)

    db_user = await crud.get_user_by_username(db, username=user.username)

    if not db_user:
        logger.warning("Пользователь %s не найден", user.username)

        raise HTTPException(status_code=400, detail="Пользователь не найден")

    logger.info("Пользователь %s найден", db_user.username)

    return db_user

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)):
    """ Аутентификация пользователя для получения токена """

    logger.debug("login_for_access_token: %s", form_data.username)
    logger.info("Попытка входа для пользователя: %s", form_data.username)

    user = await crud.get_user_by_username(db, username=form_data.username)

    if not user or not await crud.verify_password(form_data.password, user.hashed_password):
        logger.warning("Неудачная попытка входа для пользователя: %s", form_data.username)

        raise HTTPException(status_code=400, detail="Неверные учетные данные")

    access_token = auth.create_access_token(data={"sub": user.id})
    logger.info("Пользователь вошел в систему: %s", user.username)

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/change-password", response_model=schemas.UserOut)
async def change_password(
    password_change: schemas.PasswordChange,
    current_user: models.User = Depends(auth.get_current_user),
    db: AsyncSession = Depends(get_db)) -> models.User:
    """ Смена пароля """

    logger.debug("change_password: %s", current_user)
    logger.info("Попытка смены пароля для пользователя: %s", current_user.username)

    if not await crud.verify_password(password_change.old_password, current_user.hashed_password):
        logger.warning("Неудачная попытка смены пароля для пользователя: %s", current_user.username)

        raise HTTPException(status_code=400, detail="Неверный текущий пароль")

    updated_user = await crud.update_password(db, current_user, password_change.new_password)
    logger.info("Пароль изменен для пользователя: %s", current_user.username)

    return updated_user

@app.post("/verify", response_model=schemas.UserOut)
async def verify(
    current_user: models.User = Depends(auth.get_current_user)) -> models.User:
    """ Проверка пользователя по токену """

    logger.debug("verify: %s", current_user)
    logger.info("Пользователь %s верифицирован", current_user.username)

    return current_user
