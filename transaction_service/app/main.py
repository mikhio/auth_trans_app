""" Микросервис для проведения транзакций между пользователями """

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from . import external_auth, schemas, crud, models
from .database import get_db
from .logger import logger

from .config import DEFAULT_TRANSACTION_LIMIT


app = FastAPI(title="Transaction Microservice")

@app.post("/transfer", response_model=schemas.TransactionOut)
async def transfer_funds(
    transaction: schemas.TransactionCreate,
    current_user: schemas.User = Depends(external_auth.valid_token),
    db: AsyncSession = Depends(get_db)
) -> schemas.TransactionOut:
    """Проведение перевода средств"""

    logger.debug("transfer_funds: %s", transaction)
    logger.info("Пользователь %s хочет перевести %s пользователю %s",
                current_user.username,
                transaction.amount,
                transaction.receiver_username)

    # Проверка регистрации получателя
    reciver_uid = await external_auth.fetch_user(transaction.receiver_username)

    # Проверка существования отправителя
    current_account: models.Account | None = await crud.get_account_by_username(
        db,
        username=current_user.username)

    if not current_account:
        logger.info("Создание аккаунта пользователю %s", current_user.username)

        current_account = await crud.create_account(db, schemas.AccountCreate(
                                    uid=current_user.uid,
                                    username=current_user.username))

    # Проверка существования получателя
    receiver: models.Account | None = await crud.get_account_by_username(
        db,
        username=transaction.receiver_username)

    if not receiver:
        logger.info("Создание аккаунта пользователю %s", receiver.username)

        receiver = await crud.create_account(db, schemas.AccountCreate(
                                    uid=reciver_uid,
                                    username=transaction.receiver_username))

    # Проверка достаточности средств
    if current_account.balance < transaction.amount:
        logger.warning(
            "Перевод неудачен: недостаточно средств у пользователя %s",
            current_user.username)

        raise HTTPException(status_code=400, detail="Недостаточно средств")

    # Проведение транзакции
    new_transaction = await crud.create_transaction(
        db,
        sender=current_account,
        receiver=receiver,
        amount=transaction.amount)

    logger.info(
        "Пользователь %s перевёл %s пользователю %s",
        current_account.username, transaction.amount, receiver.username)

    return new_transaction

@app.get("/transactions", response_model=list[schemas.TransactionOut])
async def get_transactions(
    skip: int = 0,
    limit: int = DEFAULT_TRANSACTION_LIMIT,
    current_user: schemas.User = Depends(external_auth.valid_token),
    db: AsyncSession = Depends(get_db)
) -> list[schemas.TransactionOut]:
    """Получение истории транзакций"""

    logger.debug("get_transactions: skip=%s, limit=%s, user=%s",
                 skip, limit, current_user)
    logger.info("Пользователь %s запросил историю транзакций", current_user.username)

    # Проверка существования пользователя
    current_account: models.Account | None = await crud.get_account_by_username(
        db,
        username=current_user.username)
    if not current_account:
        logger.warning("Пользователь %s не найден", current_user.username)

        raise HTTPException(status_code=404, detail="Пользователь не найден")

    transactions: list[models.Transaction] = await crud.get_user_transactions(
        db,
        account_id=current_account.id,
        skip=skip,
        limit=limit)

    logger.info("Отправили пользователю %s историю транзакций", current_account.username)

    return transactions
