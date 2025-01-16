# auth_service/Dockerfile

# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# # Выполняем миграции
# RUN alembic upgrade head

# Команда для запуска приложения
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
