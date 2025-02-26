from aiogram import Router, types
from config import TOPICS

router = Router()

FAQ_TOPIC_ID = TOPICS["правила"]

@router.message(lambda message: message.message_thread_id == FAQ_TOPIC_ID)
async def auto_faq_menu(message: types.Message):
    """Авто-меню в разделе FAQ"""
    faq_text = (
        "📌 Часто задаваемые вопросы:\n"
        "1️⃣ Как поддержать проект?\n"
        "2️⃣ Как проверить оплату?\n"
        "3️⃣ Что делать, если есть вопросы?"
    )
    await message.answer(faq_text)
