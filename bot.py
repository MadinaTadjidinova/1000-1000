import asyncio
import logging
from aiogram import Dispatcher, types
from config import sponsor_bot, admin_bot

from handlers.reports import router as reports_router
from handlers.faq import router as faq_router
from handlers.auto_payments import auto_send_payment_reminder

from payments.payment_processing import pay_router as payments_router
from payments.payment_approval import router as payment_approval_router


from feedback import router as feedback_router 

from handlers.send_message import router as send_message_router  # Подключаем отправку сообщений

# ✅ Настраиваем глобальное логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
dp_sponsor = Dispatcher()
dp_admin = Dispatcher()

dp_admin.include_router(reports_router)
dp_admin.include_router(faq_router)
dp_admin.include_router(send_message_router)  # Добавляем router сюда после объявления dp_admin
dp_admin.include_router(payment_approval_router) 

dp_sponsor.include_router(feedback_router)
dp_sponsor.include_router(payments_router)

async def main():
    logging.info("🔄 Запуск бота...")
    asyncio.create_task(auto_send_payment_reminder(admin_bot))

    await asyncio.gather(
        dp_sponsor.start_polling(sponsor_bot),
        dp_admin.start_polling(admin_bot)
    )

if __name__ == "__main__":
    asyncio.run(main())
