# from aiogram import types, Router
# from aiogram.types import CallbackQuery
# from google_sheets import update_payment_status
# from config import admin_bot, sponsor_bot

# router = Router()

# @router.callback_query(lambda c: c.data.startswith("confirm") or c.data.startswith("reject"))
# async def process_payment_review(callback: CallbackQuery):
#     """Обработка решения админа по чеку"""
#     action, user_id, amount = callback.data.split("|")

#     if action == "confirm":
#         update_payment_status(user_id, amount, "Подтверждено")
#         await callback.message.edit_caption(
#             caption=f"✅ Чек от пользователя ID: {user_id} подтвержден!\nСумма: {amount} сом."
#         )
#         await callback.answer("✅ Чек подтверждён!")

#         # 🔹 Отправляем уведомление пользователю
#         try:
#             await sponsor_bot.send_message(
#                 chat_id=user_id,
#                 text=f"✅ Ваш платеж на {amount} сом подтвержден!"
#             )
#         except Exception as e:
#             print(f"Ошибка отправки уведомления пользователю {user_id}: {e}")


#     elif action == "reject":
#         update_payment_status(user_id, amount, "Отклонено")
#         await callback.message.edit_caption(
#             caption=f"❌ Чек от пользователя ID: {user_id} отклонён!\nСумма: {amount} сом."
#         )
#         await callback.answer("❌ Чек отклонён!")

#         # 🔹 Отправляем уведомление пользователю
#         try:
#             await sponsor_bot.send_message(
#                 chat_id=user_id,
#                 text=f"❌ Ваш платеж на {amount} сом отклонен. Попробуйте отправить другой чек."
#             )
#         except Exception as e:
#             print(f"Ошибка отправки уведомления пользователю {user_id}: {e}")


from aiogram import Router, F
from aiogram.types import CallbackQuery
from config import admin_bot
from payment_sheets import update_payment_status
from config import admin_bot, sponsor_bot

router = Router()

@router.callback_query(F.data.startswith("confirm") | F.data.startswith("reject"))
async def handle_payment_decision(callback: CallbackQuery):
    action, user_id, amount = callback.data.split("|")
    status = "✅Подтверждено" if action == "confirm" else "❌Отклонено"  # ✅ сначала определяем
    username = callback.from_user.username or f"user_{user_id}"
    update_payment_status(user_id, amount, status)                   # потом используем

    await callback.message.edit_caption(
        caption=f"Чек на {amount} сом от @{username} — {status.lower()}."
    )
    await callback.answer(f"Чек {status.lower()}!")

    # (необязательно) уведомляем пользователя
    try:
        await sponsor_bot.send_message(
            chat_id=user_id,
            text=f"Ваш чек на {amount} сом {status.lower()} ✔️"
        )
    except Exception:
        pass
