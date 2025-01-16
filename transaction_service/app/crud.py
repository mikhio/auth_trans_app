""" Модуль CRUD  """

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from . import models, schemas

from .config import DEFAULT_BALANCE, DEFAULT_TRANSACTION_LIMIT


async def get_account_by_username(db: AsyncSession, username: str) -> models.Account | None:
    """Возвращает пользователя по username"""

    result = await db.execute(
        select(models.Account).where(models.Account.username == username))

    return result.scalars().first()

async def get_account_by_uid(db: AsyncSession, uid: int) -> models.Account | None:
    """Возвращает пользователя по uid """

    result = await db.execute(
        select(models.Account).where(models.Account.uid == uid))

    return result.scalars().first()

async def create_account(db: AsyncSession, account: schemas.AccountCreate) -> models.Account:
    """ Создает пользователя """

    db_account = models.Account(
        uid=account.uid,
        username=account.username,
        balance=DEFAULT_BALANCE)

    db.add(db_account)

    await db.commit()
    await db.refresh(db_account)

    return db_account

async def create_transaction(
        db: AsyncSession,
        sender: models.Account,
        receiver: models.Account,
        amount: float) -> models.Transaction:
    """Создаёт транзакцию и обновляет балансы"""

    if sender.balance < amount:
        raise ValueError("Недостаточно средств")

    # Создание транзакции
    transaction = models.Transaction(
        sender_id=sender.id,
        receiver_id=receiver.id,
        amount=amount
    )

    db.add(transaction)

    # Обновление балансов
    sender.balance -= amount
    receiver.balance += amount

    await db.commit()
    await db.refresh(transaction)

    return transaction

async def get_user_transactions(
        db: AsyncSession,
        account_id: int,
        skip: int = 0,
        limit: int = DEFAULT_TRANSACTION_LIMIT) -> list[models.Transaction]:
    """Возвращает транзакции пользователя"""

    result = await db.execute(
        select(models.Transaction).where(
            (models.Transaction.sender_id == account_id) | (models.Transaction.receiver_id == account_id)
        ).order_by(models.Transaction.timestamp.desc()).offset(skip).limit(limit)
    )

    return result.scalars().all()
