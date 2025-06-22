import os
from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

# 🔹 Боты
sponsor_bot = Bot(token=os.getenv("SPONSOR_BOT_TOKEN"))
admin_bot = Bot(token=os.getenv("ADMIN_BOT_TOKEN"))

# 🔹 Чаты
CHAT_ID = int(os.getenv("CHAT_ID"))
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS").split(',')))

# 🔹 Топики
TOPICS = {
    "онас": int(os.getenv("TOPIC_ONAS")),
    "отчёт": int(os.getenv("TOPIC_OTCHET")),
    "джентельмен": int(os.getenv("TOPIC_DG")),
    "правила": int(os.getenv("TOPIC_RULES")),
    "реквизит": int(os.getenv("TOPIC_PAY")),
    "general": int(os.getenv("TOPIC_GENERAL")),
    "проверка": int(os.getenv("TOPIC_CHECK")),
}

# 🔹 Напоминание
PAYMENT_REMINDER = os.getenv("PAYMENT_REMINDER")
