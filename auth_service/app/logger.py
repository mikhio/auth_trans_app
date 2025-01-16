""" Модуль логгирования """

import os
import logging

from .env import LOGS_DIR

os.makedirs(LOGS_DIR, exist_ok=True)

logger = logging.getLogger("auth_service")
logger.setLevel(logging.INFO)

log_file = os.path.join(LOGS_DIR, "auth_service.log")

handler = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
