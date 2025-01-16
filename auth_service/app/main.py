""" Микросервис аунтетификации """

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from . import models, schemas, crud, auth
from .database import engine
from .logger import logger


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Microservice")

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(auth.get_db)) -> models.User:
    """ Регистрация пользователя """

    db_user = crud.get_user_by_username(db, username=user.username)

    if db_user:
        logger.info("Регистрация неудачна: пользователь %s уже существует", user.username)
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    db_user = crud.create_user(db, user)

    logger.info("Пользователь зарегистрирован: %s", db_user.username)

    return db_user

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(auth.get_db)):
    """ Аунтетификация по токену """

    user = crud.get_user_by_username(db, username=form_data.username)

    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        logger.info("Неудачная попытка входа для пользователя: %s", form_data.username)
        raise HTTPException(status_code=400, detail="Неверные учетные данные")

    access_token = auth.create_access_token(data={"sub": user.id})

    logger.info("Пользователь вошел в систему: %s", user.username)

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/change-password", response_model=schemas.UserOut)
def change_password(
    password_change: schemas.PasswordChange,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(auth.get_db)):
    """ Смена пароля """

    if not crud.verify_password(password_change.old_password, current_user.hashed_password):
        logger.info("Неудачная попытка смены пароля для пользователя: %s", current_user.username)
        raise HTTPException(status_code=400, detail="Неверный текущий пароль")

    updated_user = crud.update_password(db, current_user, password_change.new_password)
    logger.info("Пароль изменен для пользователя: %s", current_user.username)

    return updated_user
