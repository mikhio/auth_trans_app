""" Модуль для работы с базой данных """

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .env import DATABASE_URL
from .logger import logger

logger.info("Create engine to url: %s", DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
