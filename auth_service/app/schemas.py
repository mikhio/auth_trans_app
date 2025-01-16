""" Объявление схем Pydantic """

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    """ Схема создания пользователя """

    username: str
    email: EmailStr
    password: str

    # Дополнительный пример использования валидатора
    @field_validator('password')
    def validate_password(cls, value): # pylint: disable=no-self-argument
        """ Проверка пароля на длину """

        if len(value) < 8:
            raise ValueError('Пароль должен быть не короче 8 символов')

        return value

class UserOut(BaseModel):
    """ Схема возвращаемого пользователя """

    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = {
        "from_attributes": True 
    }

class Username(BaseModel):
    """ Схема имени пользователя """

    username: str

class UserFound(BaseModel):
    """ Схема найденного пользователя """

    id: int
    username: str


class Token(BaseModel):
    """ Схема токена """

    access_token: str
    token_type: str

class TokenData(BaseModel):
    """ Схема доп. данных токена """

    user_id: Optional[int] = None

class PasswordChange(BaseModel):
    """ Схема смены пароля """

    old_password: str
    new_password: str
