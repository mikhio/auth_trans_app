""" Модуль для работы с переменными окружения """

import os
from dotenv import load_dotenv

# Путь к .env файлу
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=env_path)

# Переменные окружения
LOGS_DIR = os.getenv("LOGS_DIR", "/app/logs")
DATABASE_URL = os.getenv("TRANS_DATABASE_URL")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")

# Проверка обязательных переменных
if not DATABASE_URL:
    raise ValueError("TRANS_DATABASE_URL не установлена в переменных окружения")

if not AUTH_SERVICE_URL:
    raise ValueError("AUTH_SERVICE_URL не установлена в переменных окружения")
