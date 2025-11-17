# Базовый образ
FROM python:3.12-slim

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt


# Копируем исходный код приложения
COPY src/ ./src/

# Копирует файл окружения
COPY .env.default .env

# Создаем папку для ключей
RUN mkdir /keys

# Указываем порт
EXPOSE 8001

# Запускаем приложение
CMD ["uvicorn", "src.presentation.app:app", "--host", "0.0.0.0", "--port", "8000"]