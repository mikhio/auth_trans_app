""" Модуль для загрузки env переменных """

import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '..','.env')

load_dotenv(dotenv_path=env_path)

LOGS_DIR = os.getenv("AUTH_LOGS_DIR", "/app/logs")

DATABASE_URL = os.getenv("AUTH_DATABASE_URL")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM  = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


if not DATABASE_URL:
    raise ValueError("DATA_BASE_URL не установлена в переменных окружения")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY не установлена в переменных окружения")
