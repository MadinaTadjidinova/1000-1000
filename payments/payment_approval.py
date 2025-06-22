from aiogram import Router, F
from aiogram.types import CallbackQuery
from config import admin_bot, sponsor_bot
from payment_sheets import update_payment_status_by_id

router = Router()

@router.callback_query(F.data.startswith("confirm") | F.data.startswith("reject"))
async def handle_payment_decision(callback: CallbackQuery):
    action, check_id = callback.data.split("|")
    status = "✅Подтверждено" if action == "confirm" else "❌Отклонено"

    # Обновляем статус в таблице по ID
    update_payment_status_by_id(check_id, status)

    # Обновляем сообщение в админ-группе
    caption = callback.message.caption or ""
    new_caption = caption + f"\n\nСтатус: {status}"
    await callback.message.edit_caption(caption=new_caption)

    await callback.answer(f"Чек {status.lower()}!")

    # Уведомляем пользователя, если возможно
    try:
        user_id = int(check_id.split("-")[0])  # Если в check_id есть user_id (можно иначе)
        await sponsor_bot.send_message(
            chat_id=user_id,
            text=f"Ваш чек {status.lower()} ✔️"
        )
    except Exception:
        pass
