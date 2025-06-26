from aiogram import Router, types, Bot, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import CHAT_ID, TOPICS


router = Router()
FAQ_TOPIC_ID = TOPICS["правила"]

# 🔹 Главное меню
def get_main_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📜 Правила", callback_data="menu_rules")],
            [InlineKeyboardButton(text="📄 Джентльменское соглашение", callback_data="menu_dj")],
            [InlineKeyboardButton(text="❓ FAQ", callback_data="menu_faq")],
        ]
    )

# 🔹 Подменю "Правила"
def get_rules_submenu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1️⃣ Общие положения", callback_data="rule_1")],
            [InlineKeyboardButton(text="2️⃣ Принципы сообщества", callback_data="rule_2")],
            [InlineKeyboardButton(text="3️⃣ Формы поддержки", callback_data="rule_3")],
            # [InlineKeyboardButton(text="4️⃣ Джентльмендик келишим / Джентльменское соглашение", callback_data="rule_4")],
            [InlineKeyboardButton(text="4️⃣ Права и привилегии", callback_data="rule_4")],
            [InlineKeyboardButton(text="5️⃣ Отчетность и контроль", callback_data="rule_5")],
            [InlineKeyboardButton(text="6️⃣ Завершение участия", callback_data="rule_6")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
        ]
    )

# 🔹 Подменю FAQ
def get_faq_submenu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💸 Как оплатить?", callback_data="faq_1")],
            [InlineKeyboardButton(text="🔓 Как получить доступ?", callback_data="faq_2")],
            [InlineKeyboardButton(text="❤️ Как поддержать проект?", callback_data="faq_3")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
        ]
    )

# 🔹 Подменю FAQ
def get_dj_submenu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
        ]
    )

# 🔹 Тексты для разделов правил
RULES_TEXT = {
    "rule_1": "📘 **1. Общие положения**\n\n"
              "Сообщество спонсоров библиотеки «Дем» создано для поддержки образовательных, культурных и социальных инициатив. "
              "Проект «1000/1000» предполагает участие 1000 спонсоров, каждый из которых вносит вклад от 1000 сомов и выше в развитие библиотеки.",

    "rule_2": "📘 **2. Принципы сообщества**\n\n"
              "🔹 Прозрачность — вся информация о расходах доступна участникам.\n"
              "🔹 Добровольность — участие полностью добровольное и не обязывает.\n"
              "🔹 Открытость — каждый спонсор может предлагать идеи.\n"
              "🔹 Взаимоуважение — запрещены неуважение, дискриминация и агрессия.",

    "rule_3": "📘 **3. Формы поддержки**\n\n"
              "💸 Финансовая поддержка (разовая или регулярная).\n"
              "📚 Материальная помощь (книги, оборудование, мебель и т.д.).\n"
              "📣 Информационная поддержка (продвижение, привлечение участников).\n"
              "🤝 Волонтёрская помощь (мероприятия, лекции, мастер-классы).",

    "rule_4": 
              "📊 Доступ к отчётам\n"
              "🎟️ Приглашения на закрытые мероприятия\n"
              "🎖️ Благодарственные письма и признание\n"
              "🧠 Участие в стратегическом планировании.",

    "rule_5": "📘 **5. Отчетность и контроль**\n\n"
              "Отчёты публикуются раз в квартал в двух форматах: финансовые (в Telegram) и фото/видео с мероприятий.",

    "rule_6": "📘 **6. Завершение участия**\n\n"
              "Спонсор может выйти в любой момент. При нарушении правил - возможен выход из проекта.\n\n"
              "💙📚 Спасибо за вашу поддержку!"
}

DJ_TEXT = {
    "menu_dj": "📘 **1. Общие положения**\n\n"
              "Сообщество спонсоров библиотеки «Дем» создано для поддержки образовательных, культурных и социальных инициатив. "
              "Проект «1000/1000» предполагает участие 1000 спонсоров, каждый из которых вносит вклад от 1000 сомов и выше в развитие библиотеки.",
}

# 🔹 Тексты для FAQ
FAQ_TEXT = {
    "faq_1": "💸 Как оплатить?**\n\n"
             "Перейдите в топик 'Реквизиты' или спросите у администратора.",

    "faq_2": "❤️ Как поддержать проект?**\n\n"
             "Вы можете ежемесячно вносить 1000 сом или больше в фонд библиотеки."
}
FAQ_TEXT = {
    "faq_1": "💸 Как оплатить?**\n\n"
             "Перейдите в топик 'Стать потроном' или спросите у администратора.",

    "faq_2": "🔓 Как получить доступ?**\n\n"
             "После оплаты напишите администратору — он подтвердит и откроет доступ.",

    "faq_3": "❤️ Как поддержать проект?**\n\n"
             "Вы можете ежемесячно вносить 1000 сом или больше в фонд библиотеки."
}


# ✅ Отображение главного меню при сообщении в топике
@router.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📢 *Кош келиңиз! Бөлүмдү тандаңыз*\n*Добро пожаловать! Выберите раздел:*",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

# ✅ Переход в подменю Правил
@router.callback_query(lambda c: c.data == "menu_rules")
async def show_rules_menu(callback: types.CallbackQuery):
    await callback.message.edit_text("📘 *Коомчулуктун эрежелери / Правила сообщества:* Бөлүмдү тандаңыз / Выберите раздел:",
                                     reply_markup=get_rules_submenu_keyboard(), parse_mode="Markdown")
    await callback.answer()

@router.callback_query(lambda c: c.data == "menu_rules")
async def show_rules_menu(callback: types.CallbackQuery):
    await callback.message.edit_text("📘 *Коомчулуктун эрежелери / Правила сообщества:* Бөлүмдү тандаңыз / Выберите раздел:",
                                     reply_markup=get_dj_submenu_keyboard(), parse_mode="Markdown")
    await callback.answer()

# ✅ Переход в подменю FAQ
@router.callback_query(lambda c: c.data == "menu_faq")
async def show_faq_menu(callback: types.CallbackQuery):
    await callback.message.edit_text("❓ *Часто задаваемые вопросы:* Выберите интересующий вопрос:",
                                     reply_markup=get_faq_submenu_keyboard(), parse_mode="Markdown")
    await callback.answer()

# ✅ Обработка разделов Правил
@router.callback_query(lambda c: c.data in RULES_TEXT)
async def show_rule(callback: types.CallbackQuery):
    await callback.message.edit_text(RULES_TEXT[callback.data],
                                     reply_markup=get_rules_submenu_keyboard(), parse_mode="Markdown")
    await callback.answer()

# ✅ Обработка разделов FAQ
@router.callback_query(lambda c: c.data in FAQ_TEXT)
async def show_faq(callback: types.CallbackQuery):
    await callback.message.edit_text(FAQ_TEXT[callback.data],
                                     reply_markup=get_faq_submenu_keyboard(), parse_mode="Markdown")
    await callback.answer()

# ✅ Обработка разделов DJ
@router.callback_query(lambda c: c.data in DJ_TEXT)
async def show_rule(callback: types.CallbackQuery):
    await callback.message.edit_text(DJ_TEXT[callback.data],
                                     reply_markup=get_dj_submenu_keyboard(), parse_mode="Markdown")
    await callback.answer()

# ✅ Возврат в главное меню
@router.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📢 Кош келиңиз! Бөлүмдү тандаңыз\nДобро пожаловать! Выберите раздел:",
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()

@router.message(F.text == "/menu")
async def handle_menu_command(message: Message, bot: Bot):
    await bot.send_message(
        chat_id=CHAT_ID,
        text="📢 Добро пожаловать! Выберите раздел:",
        reply_markup=get_main_menu_keyboard(),
        message_thread_id=FAQ_TOPIC_ID
    )
