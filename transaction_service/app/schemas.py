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

    def __repr__(self):
        return f"AccountCreate(uid={self.uid}, username={self.username})"

class TransactionCreate(BaseModel):
    """Схема создания транзакции"""

    receiver_username: str = Field(..., example="anotheruser")
    amount: float = Field(..., gt=0, example=100.0)

    def __repr__(self):
        return f"TransactionCreate(receiver_username={self.receiver_username}, amount={self.amount})"

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

    def __repr__(self):
        return ("TransactionOut("
            f"id={self.id},"
            f"sender_id={self.sender_id},"
            f"receiver_id={self.receiver_id},"
            f"amount={self.amount},"
            f"timestamp={self.timestamp})")

class User(BaseModel):
    """Схема пользователя"""

    uid: int
    username: str

    model_config = {
        "from_attributes": True
    }

    def __repr__(self):
        return f"User(uid={self.uid}, username={self.username})"

class Username(BaseModel):
    """Схема имени пользователя"""

    username: str

    model_config = {
        "from_attributes": True
    }

    def __repr__(self):
        return f"Username(username={self.username})"
