import asyncio
import logging
from aiogram import Dispatcher
from config import sponsor_bot, admin_bot

from handlers.reports import router as reports_router
from handlers.faq import router as faq_router
from handlers.auto_payments import auto_send_payment_reminder
from payments.payment_processing import pay_router as payments_router
from payments.payment_approval import router as payment_approval_router
from feedback import router as feedback_router
from handlers.send_message import router as send_message_router
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# ✅ Логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ Диспетчеры
dp_sponsor = Dispatcher()
dp_admin = Dispatcher()

# ✅ Подключение роутеров
dp_admin.include_router(reports_router)
dp_admin.include_router(faq_router)
dp_admin.include_router(send_message_router)
dp_admin.include_router(payment_approval_router)

dp_sponsor.include_router(feedback_router)
dp_sponsor.include_router(payments_router)

# ✅ Главная функция запуска
async def main():
    logging.info("🔄 Запуск бота...")
    asyncio.create_task(auto_send_payment_reminder(admin_bot))  # Фоновая задача

    await asyncio.gather(
        dp_sponsor.start_polling(sponsor_bot),
        dp_admin.start_polling(admin_bot)
    )

if __name__ == "__main__":
    asyncio.run(main())
