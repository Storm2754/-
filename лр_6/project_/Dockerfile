# Используем базовый образ Python
FROM python:3.9-slim-buster

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем приложение
COPY . .

# Запускаем приложение при старте контейнера
CMD ["python", "server.py"]