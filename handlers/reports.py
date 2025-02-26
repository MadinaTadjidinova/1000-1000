import os
import logging
from aiogram import Bot, types, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, InputMediaDocument
from config import CHAT_ID, TOPICS

router = Router()

REPORT_TOPIC_ID = TOPICS.get("отчёт", None)
REPORTS_DIR = "reports"
REPORT_MESSAGE_ID = None  # ID сообщения с отчетами

if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

# Генерация кнопок для выбора отчета
def get_reports_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Отчет мероприятий", callback_data="show_events_report")],
            [InlineKeyboardButton(text="💰 Финансовый отчет", callback_data="show_finance_report")]
        ]
    )

@router.message(lambda message: message.document and message.caption and message.caption.startswith("/upload_report"))
async def handle_report_upload(message: types.Message, bot: Bot):
    """Обновляет файл отчета, НЕ отправляя новое сообщение"""
    global REPORT_MESSAGE_ID

    args = message.caption.split()
    if len(args) < 2 or args[1] not in ["events", "finance"]:
        await message.answer("❌ Используйте команду: `/upload_report events` или `/upload_report finance`.")
        return

    report_type = args[1]
    file_path = os.path.join(REPORTS_DIR, f"{report_type}.pdf")

    await bot.download(file=message.document, destination=file_path)

    document = FSInputFile(file_path)
    caption = "📄 Доступны отчеты: выберите нужный файл."

    if REPORT_MESSAGE_ID:
        try:
            await bot.edit_message_media(
                chat_id=CHAT_ID,
                message_id=REPORT_MESSAGE_ID,
                media=InputMediaDocument(media=document, caption=caption),
                reply_markup=get_reports_keyboard()
            )
        except Exception as e:
            logging.error(f"Ошибка при обновлении отчета: {e}")
            await message.answer("⚠ Ошибка при обновлении сообщения, попробуйте еще раз.")
    else:
        msg = await bot.send_document(
            chat_id=CHAT_ID,
            document=document,
            caption=caption,
            message_thread_id=REPORT_TOPIC_ID,
            reply_markup=get_reports_keyboard()
        )
        REPORT_MESSAGE_ID = msg.message_id

    await message.delete()

@router.callback_query(lambda c: c.data in ["show_events_report", "show_finance_report"])
async def report_callback_handler(callback: types.CallbackQuery):
    """При нажатии на кнопку отчет обновляется в одном сообщении"""
    global REPORT_MESSAGE_ID

    report_type = "events" if callback.data == "show_events_report" else "finance"
    file_path = os.path.join(REPORTS_DIR, f"{report_type}.pdf")

    if not os.path.exists(file_path):
        await callback.answer("❌ Отчет не найден. Администратор должен загрузить новый файл.", show_alert=True)
        return

    document = FSInputFile(file_path)
    caption = "📄 Доступны отчеты: выберите нужный файл."

    if REPORT_MESSAGE_ID:
        try:
            await callback.bot.edit_message_media(
                chat_id=CHAT_ID,
                message_id=REPORT_MESSAGE_ID,
                media=InputMediaDocument(media=document, caption=caption),
                reply_markup=get_reports_keyboard()
            )
        except Exception as e:
            logging.error(f"Ошибка при обновлении отчета: {e}")
            await callback.answer("⚠ Ошибка обновления сообщения, попробуйте позже.", show_alert=True)

    await callback.answer()
