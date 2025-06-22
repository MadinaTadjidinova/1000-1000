from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from config import sponsor_bot, admin_bot, ADMIN_CHAT_ID

router = Router()

FEEDBACK_TOPIC_ID = 238  # Заменить на актуальный ID темы "Отзывы"

@router.message(Command("feedback"))
async def send_feedback_to_admins(message: types.Message, command: CommandObject):
    """Обработка отзыва и отправка в админскую группу"""
    feedback_text = command.args.strip() if command.args else None

    if not feedback_text:
        await message.answer(
            "❌ Пожалуйста, используйте формат:\n`/feedback Ваш отзыв`",
            parse_mode="Markdown"
        )
        return

    user = message.from_user
    username_link = f"[{user.full_name}](tg://user?id={user.id})"

    feedback_message = (
        f"📩 *Новый отзыв от пользователя!*\n\n"
        f"👤 *Пользователь:* {username_link}\n"
        f"💬 *Сообщение:*\n{feedback_text}"
    )

    await admin_bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        message_thread_id=FEEDBACK_TOPIC_ID,
        text=feedback_message,
        parse_mode="Markdown"
    )

    await message.answer("✅ Ваш отзыв отправлен администраторам. Спасибо за обратную связь!")
