# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем Docker CLI и обновляем систему
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean

# Устанавливаем зависимости Python
RUN pip install flask

# Копируем наш код в контейнер
COPY app.py /app/app.py

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем переменные окружения (можно заменить или задать при запуске контейнера)
ENV CONTAINER1=gov-portal-verifier
ENV CONTAINER2=gov-portal-db

# Открываем порт, если нужно для доступа извне контейнера
EXPOSE 5017

# Запускаем приложение
CMD ["python", "app.py"]
