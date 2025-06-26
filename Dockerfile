FROM python:3.10-slim

# Установка Tesseract и системных библиотек
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean

# Рабочая директория
WORKDIR /app

# Копируем всё
COPY . .

# Установка Python-зависимостей
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Команда запуска
CMD ["python", "bot.py"]
