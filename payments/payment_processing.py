# import os
# from aiogram import types, Router
# from aiogram.types import FSInputFile
# from config import admin_bot, TOPICS, ADMIN_CHAT_ID, sponsor_bot
# from google_sheets import add_payment
# from handlers.receipt_validation import validate_receipt
# from handlers.admin_buttons import get_admin_buttons

# pay_router = Router()

# RECEIPTS_FOLDER = "receipts"
# if not os.path.exists(RECEIPTS_FOLDER):
#     os.makedirs(RECEIPTS_FOLDER)

# @pay_router.message()
# async def pay_handler(message: types.Message):
#     """Обрабатываем фото чека от пользователя."""
    
#     if not message.photo:
#         await message.answer("❌ Чтобы отправить отзыв, используйте `/feedback [ваш текст]`\n" "💰 Чтобы отправить чек, прикрепите фото и напишите сумму (например, `1000`).")
#         return

#     if not message.caption:
#         await message.answer("❌ Укажите сумму в описании к изображению.")
#         return
    
#     args = message.caption.split()
#     if len(args) < 1:
#         await message.answer("❌ Используйте формат: `1000` (только сумма)")
#         return

#     amount = args[0]
#     user_id = message.from_user.id
#     username = message.from_user.username or f"user_{user_id}"

#     # 📸 Получаем файл чека
#     file_id = message.photo[-1].file_id
#     file_info = await message.bot.get_file(file_id)
#     file_path = file_info.file_path
#     local_path = os.path.join(RECEIPTS_FOLDER, f"{file_id}.jpg")

#     try:
#         await message.bot.download_file(file_path, local_path)
#         is_valid, validation_message = validate_receipt(local_path, amount)

#         if is_valid:
#             add_payment(user_id, username, amount, "Чек", "Подтверждено")
#             await message.answer(f"✅ Чек автоматически подтверждён! Сумма: {amount} сом.")
#         else:
#             add_payment(user_id, username, amount, "Чек (на проверке)", "Ожидание")
#             markup = get_admin_buttons(user_id, amount)

#             await admin_bot.send_photo(
#                 chat_id=ADMIN_CHAT_ID,  # ✅ Осталось как есть
#                 message_thread_id=TOPICS["проверка"],
#                 photo=FSInputFile(local_path),
#                 caption=f"❗ Подозрительный чек от @{username}.\nПричина: {validation_message}",
#                 reply_markup=markup
#             )

#             await message.answer("🔍 Ваш чек отправлен на проверку админам. Ожидайте подтверждения.")

#     except Exception as e:
#         await message.answer(f"⚠ Ошибка при обработке чека: {str(e)}")