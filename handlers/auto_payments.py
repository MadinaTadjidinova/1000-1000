import asyncio
import logging
from config import PAYMENT_REMINDER, CHAT_ID
from aiogram import Bot

async def auto_send_payment_reminder(bot: Bot):
    """Автоматически отправляет напоминание о платеже 1-го и 27-го числа месяца (один раз в день)."""
    already_sent = set()

    while True:
        now = datetime.now()
        day = now.day
        date_key = now.strftime("%Y-%m-%d")

        if day in [1, 27] and date_key not in already_sent:
            try:
                await bot.send_message(CHAT_ID, PAYMENT_REMINDER)
                logging.info(f"📅 Напоминание отправлено: {date_key}")
                already_sent.add(date_key)
            except Exception as e:
                logging.error(f"❌ Ошибка отправки напоминания: {e}")

        await asyncio.sleep(3600)  # Проверка каждый час