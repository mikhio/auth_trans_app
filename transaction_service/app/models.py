""" Модели данных для работы с транзакциями и аккаунтами пользователей """

from datetime import datetime

from sqlalchemy import Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

func: callable


class Base(DeclarativeBase):
    """Базовая модель"""

class Transaction(Base):
    """Модель транзакции"""

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    sender_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)

    amount: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    sender: Mapped["Account"] = relationship("Account", foreign_keys=[sender_id])
    receiver: Mapped["Account"] = relationship("Account", foreign_keys=[receiver_id])

    def __repr__(self) -> str:
        return (
            "Transaction("
            f"id={self.id!r}, "
            f"sender={self.sender!r}, "
            f"receiver={self.receiver!r}, "
            f"amount={self.amount!r})"
        )

class Account(Base):
    """ Модель аккаунта пользователя c балансом """

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    uid: Mapped[int] = mapped_column(unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)

    balance: Mapped[float] = mapped_column(default=0.0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now())

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, balance={self.balance!r})"
