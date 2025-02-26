from aiogram import Router, types
from aiogram.filters import Command
from config import admin_bot, CHAT_ID, TOPICS, ADMIN_IDS

router = Router()


@router.message(Command("send"))
async def send_to_topic(message: types.Message):

    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас нет прав на отправку сообщений.")
        return

    # Если сообщение содержит фото, видео или документ — берем caption, иначе обычный текст
    raw_text = message.caption if message.caption else message.text
    args = raw_text.split(maxsplit=2) if raw_text else []

    if not raw_text:
        await message.answer("❌ Укажите текст сообщения после команды /send.")
        return

    if len(args) < 2:
        await message.answer("❌ Используйте формат: `/send [топик] [текст]` или прикрепите медиа.")
        return

    topic_name = args[1].lower()
    text = args[2] if len(args) > 2 else None  

    if topic_name not in TOPICS:
        await message.answer(f"❌ Ошибка: топик `{topic_name}` не найден. Доступные: {', '.join(TOPICS.keys())}")
        return

    topic_id = TOPICS[topic_name]

    # Если топик "general", `message_thread_id` не нужен
    message_kwargs = {"chat_id": CHAT_ID, "caption": text}
    if topic_name != "general":
        message_kwargs["message_thread_id"] = topic_id

    # Отправка медиа (фото, видео, документ)
    try:
        # Отправка медиа
        if message.photo:
            await admin_bot.send_photo(**message_kwargs, photo=message.photo[-1].file_id)
        elif message.video:
            await admin_bot.send_video(**message_kwargs, video=message.video.file_id)
        elif message.document:
            await admin_bot.send_document(**message_kwargs, document=message.document.file_id)
        elif message.voice:
            await admin_bot.send_voice(**message_kwargs, voice=message.voice.file_id)
        elif message.audio:
            await admin_bot.send_audio(**message_kwargs, audio=message.audio.file_id)
        elif text:
            # Если есть только текст
            await admin_bot.send_message(CHAT_ID, text, message_thread_id=topic_id if topic_name != "general" else None)
        else:
            await message.answer("❌ Ошибка: вы не прикрепили ни медиа, ни текст.")
            return

        await message.answer(f"✅ Сообщение успешно отправлено в **{topic_name}**!")

    except Exception as e:
        await message.answer(f"⚠ Ошибка при отправке сообщения: {e}")