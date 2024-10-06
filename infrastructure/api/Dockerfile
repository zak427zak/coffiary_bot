# Используем Python как базовый образ
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /usr/src/app/api

# Устанавливаем необходимые пакеты для локали
RUN apt-get update && apt-get install -y locales && \
    echo "ru_RU.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Устанавливаем переменные окружения для локали
ENV LANG=ru_RU.UTF-8
ENV LANGUAGE=ru_RU:ru
ENV LC_ALL=ru_RU.UTF-8

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходники приложения
COPY . .

# Команда для запуска приложения
CMD ["python3", "app.py"]
