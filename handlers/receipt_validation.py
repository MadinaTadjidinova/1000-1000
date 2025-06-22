import os
import pytesseract
from PIL import Image
from aiogram import types, Router
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from config import admin_bot, TOPICS
from payment_sheets import add_payment  

pay_router = Router()

RECEIPTS_FOLDER = "receipts"
if not os.path.exists(RECEIPTS_FOLDER):
    os.makedirs(RECEIPTS_FOLDER)

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    return pytesseract.image_to_string(img, lang="eng+rus")

def validate_receipt(image_path, expected_amount):
    text = extract_text_from_image(image_path)
    return str(expected_amount) in text, "Сумма не найдена в чеке."

def get_admin_buttons(user_id, amount):
    """Создаёт inline-кнопки для подтверждения/отклонения чека"""
    buttons = [
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"confirm|{check_id}")],
        [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject|{check_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@pay_router.message()
async def pay_handler(message: types.Message):
    if not message.photo or not message.caption:
        await message.answer("❌ Отправьте фото чека и укажите сумму в описании.")
        return

    amount = message.caption.split()[0]
    user_id = message.from_user.id
    username = message.from_user.username or f"user_{user_id}"

    file_id = message.photo[-1].file_id
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    local_path = os.path.join(RECEIPTS_FOLDER, f"{file_id}.jpg")

    await message.bot.download_file(file_path, local_path)
    is_valid, validation_message = validate_receipt(local_path, amount)

    if is_valid:
        add_payment(user_id, username, amount, "Чек", "Подтверждено")
        await message.answer(f"✅ Чек автоматически подтверждён! Сумма: {amount} сом.")
    else:
        await admin_bot.send_photo(
            chat_id=TOPICS["проверка"],
            photo=FSInputFile(local_path),
            caption=f"❗ Подозрительный чек от @{username}.\nПричина: {validation_message}",
            reply_markup=get_admin_buttons(user_id, amount)
        )
        await message.answer("🔍 Ваш чек отправлен на проверку админам.")
