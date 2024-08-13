# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем зависимости
RUN pip install flask

# Копируем наш код в контейнер
COPY app.py /app/app.py

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем переменные окружения (можно заменить или задать при запуске контейнера)
ENV CONTAINER1=gov-portal-verifier
ENV CONTAINER2=gov-portal-db

# Запускаем приложение
CMD ["python", "app.py"]
