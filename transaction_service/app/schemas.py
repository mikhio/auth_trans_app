""" Модуль схем для валидации данных """

from datetime import datetime

from pydantic import BaseModel, Field

class AccountCreate(BaseModel):
    """Схема пользователя (ограниченная информация)"""

    uid: int
    username: str

    model_config = {
        "from_attributes": True
    }

class TransactionCreate(BaseModel):
    """Схема создания транзакции"""

    receiver_username: str = Field(..., example="anotheruser")
    amount: float = Field(..., gt=0, example=100.0)

class TransactionOut(BaseModel):
    """Схема возвращаемой транзакции"""

    id: int
    sender_id: int
    receiver_id: int
    amount: float
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }

class User(BaseModel):
    """Схема пользователя"""

    uid: int
    username: str

    model_config = {
        "from_attributes": True
    }

class Username(BaseModel):
    """Схема имени пользователя"""

    username: str

    model_config = {
        "from_attributes": True
    }
