import asyncio
import logging
from config import PAYMENT_REMINDER, CHAT_ID
from aiogram import Bot

async def auto_send_payment_reminder(bot: Bot):
    """Автоматически отправляет напоминание о платеже 1-го и 26-го числа месяца."""
    while True:
        await asyncio.sleep(36)  # Проверять раз в час

        from datetime import datetime
        today = datetime.now().day

        if today in [1, 27]:  # Отправлять 1-го и 26-го числа
            try:
                await bot.send_message(CHAT_ID, PAYMENT_REMINDER)  # Убрали message_thread_id
                logging.info("📅 Напоминание о платеже отправлено в общий чат.")
            except Exception as e:
                logging.error(f"❌ Ошибка отправки напоминания: {e}")
