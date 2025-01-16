""" Модуль CRUD """

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import models, schemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str) -> models.User | None:
    """ Возвращает пользователя по username """

    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str) -> models.User | None:
    """ Возвращает пользователя по email """

    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """ Создает пользователя """

    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def verify_password(plain_password, hashed_password) -> bool:
    """ Проверяет пароль """

    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: Session, user_id: int) -> models.User | None:
    """ Возвращает пользователя по user_id"""

    return db.query(models.User).filter(models.User.id == user_id).first()

def update_password(db: Session, user: models.User, new_password: str) -> models.User: 
    """ Обновляет пароль """

    user.hashed_password = pwd_context.hash(new_password)

    db.commit()
    db.refresh(user)

    return user
