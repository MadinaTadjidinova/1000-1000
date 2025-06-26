from aiogram import Router, types, Bot, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import CHAT_ID, TOPICS


router = Router()
FAQ_TOPIC_ID = TOPICS["правила"]

# 🔹 Главное меню
def get_main_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📜 Эрежелер / Правила", callback_data="menu_rules")],
            [InlineKeyboardButton(text="❓ 📄 Джентльмендик келишим / Джентльменское соглашение", callback_data="menu_dj")],
            [InlineKeyboardButton(text="❓ FAQ", callback_data="menu_faq")],
        ]
    )

# 🔹 Подменю "Правила"
def get_rules_submenu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1️⃣ Жалпы жоболор / Общие положения", callback_data="rule_1")],
            [InlineKeyboardButton(text="2️⃣ Коомдун принциптери / Принципы сообщества", callback_data="rule_2")],
            [InlineKeyboardButton(text="3️⃣ Колдоо формалары / Формы поддержки", callback_data="rule_3")],
            # [InlineKeyboardButton(text="4️⃣ Джентльмендик келишим / Джентльменское соглашение", callback_data="rule_4")],
            [InlineKeyboardButton(text="4️⃣ Укуктар жана артыкчылыктар / Права и привилегии", callback_data="rule_4")],
            [InlineKeyboardButton(text="5️⃣ Отчеттуулук жана көзөмөл / Отчетность и контроль", callback_data="rule_5")],
            [InlineKeyboardButton(text="6️⃣ Катышууну токтотуу / Завершение участия", callback_data="rule_6")],
            [InlineKeyboardButton(text="⬅️ Артка / Назад", callback_data="back_to_main")]
        ]
    )

# 🔹 Подменю FAQ
def get_faq_submenu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💸 Кантип төлөөгө болот? / Как оплатить?", callback_data="faq_1")],
            [InlineKeyboardButton(text="🔓 Кандайча кирүүгө болот? / Как получить доступ?", callback_data="faq_2")],
            [InlineKeyboardButton(text="❤️ Кантип колдосо болот? / Как поддержать проект?", callback_data="faq_3")],
            [InlineKeyboardButton(text="⬅️ Артка / Назад", callback_data="back_to_main")]
        ]
    )

# 🔹 Подменю FAQ
def get_dj_submenu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Артка / Назад", callback_data="back_to_main")]
        ]
    )

# 🔹 Тексты для разделов правил
RULES_TEXT = {
    "rule_1": "📘 **1. Жалпы жоболор / Общие положения**\n\n"
              "**[KG]** «Дем» китепканасынын демөөрчүлөр коому билим берүү, маданият жана коомдук демилгелерди колдоо үчүн түзүлгөн. "
              "«1000/1000» долбоору китепкананы өнүктүрүү үчүн 1000 сом же андан көп өлчөмдө жардам берген 1000 демөөрчүнүн катышуусун камтыйт.\n\n"
              "**[RU]** Сообщество спонсоров библиотеки «Дем» создано для поддержки образовательных, культурных и социальных инициатив. "
              "Проект «1000/1000» предполагает участие 1000 спонсоров, каждый из которых вносит вклад от 1000 сомов и выше в развитие библиотеки.",

    "rule_2": "📘 **2. Коомдун принциптери / Принципы сообщества**\n\n"
              "**[KG]**\n"
              "🔹 Ачыктуулук – каражаттарды пайдалануу боюнча бардык маалыматтар коомдун мүчөлөрүнө жеткиликтүү.\n"
              "🔹 Ыктыярдуулук – катышуу ыктыярдуу жана кошумча милдеттенмелерди жүктөбөйт.\n"
              "🔹 Ачыктык – ар бир демөөрчү идея сунуштай алат.\n"
              "🔹 Өз ара урматтоо – урматсыз мамиле, дискриминация жана агрессия тыюу салынат.\n\n"
              "**[RU]**\n"
              "🔹 Прозрачность — вся информация о расходах доступна участникам.\n"
              "🔹 Добровольность — участие полностью добровольное и не обязывает.\n"
              "🔹 Открытость — каждый спонсор может предлагать идеи.\n"
              "🔹 Взаимоуважение — запрещены неуважение, дискриминация и агрессия.",

    "rule_3": "📘 **3. Колдоо формалары / Формы поддержки**\n\n"
              "**[KG]**\n"
              "💸 Каржылык колдоо (бир жолку же туруктуу).\n"
              "📚 Материалдык жардам (китептер, жабдуулар, эмерек ж.б.).\n"
              "📣 Маалыматтык колдоо (жарнама, жаңы катышуучулар).\n"
              "🤝 Ыктыярчы жардам (иш-чаралар, лекциялар, мастер-класстар).\n\n"
              "**[RU]**\n"
              "💸 Финансовая поддержка (разовая или регулярная).\n"
              "📚 Материальная помощь (книги, оборудование, мебель и т.д.).\n"
              "📣 Информационная поддержка (продвижение, привлечение участников).\n"
              "🤝 Волонтёрская помощь (мероприятия, лекции, мастер-классы).",

    # "rule_4": "📘 **4. Джентльмендик келишим / Джентльменское соглашение**\n\n"
    #           "**[KG]** Ар бир катышуучу 1 жылдык келишимге кол коёт жана ай сайын төлөм жүргүзөт. Каражаттар китепкана үчүн колдонулат.\n\n"
    #           "**[RU]** Каждый участник подписывает соглашение на 1 год и вносит ежемесячные взносы. Средства направляются на развитие библиотеки.",

    "rule_4": "📘 **4. Укуктар жана артыкчылыктар / Права и привилегии**\n\n"
              "**[KG]**\n"
              "📊 Отчетторго жеткилик\n"
              "🎟️ Жабык иш-чараларга чакыруу\n"
              "🎖️ Ыраазычылык жана таануу\n"
              "🧠 Долбоорлорду пландаштырууга катышуу\n\n"
              "**[RU]**\n"
              "📊 Доступ к отчётам\n"
              "🎟️ Приглашения на закрытые мероприятия\n"
              "🎖️ Благодарственные письма и признание\n"
              "🧠 Участие в стратегическом планировании.",

    "rule_5": "📘 **5. Отчеттуулук жана көзөмөл / Отчетность и контроль**\n\n"
              "**[KG]** Ар үч ай сайын эки форматта отчет жарыяланат: Telegram-канал аркылуу каржылык жана фото/видео отчеттор.\n\n"
              "**[RU]** Отчёты публикуются раз в квартал в двух форматах: финансовые (в Telegram) и фото/видео с мероприятий.",

    "rule_6": "📘 **6. Катышууну токтотуу / Завершение участия**\n\n"
              "**[KG]** Демөөрчү каалаган убакта долбоордон чыга алат. Эрежелер бузулса — чыгарылышы мүмкүн.\n\n"
              "**[RU]** Спонсор может выйти в любой момент. При нарушении правил — возможен выход из проекта.\n\n"
              "💙📚 Сиздин колдооңузга ыраазыбыз! / Спасибо за вашу поддержку!"
}

DJ_TEXT = {
    "menu_dj": "📘 **1. Жалпы жоболор / Общие положения**\n\n"
              "**[KG]** «Дем» китепканасынын демөөрчүлөр коому билим берүү, маданият жана коомдук демилгелерди колдоо үчүн түзүлгөн. "
              "«1000/1000» долбоору китепкананы өнүктүрүү үчүн 1000 сом же андан көп өлчөмдө жардам берген 1000 демөөрчүнүн катышуусун камтыйт.\n\n"
              "**[RU]** Сообщество спонсоров библиотеки «Дем» создано для поддержки образовательных, культурных и социальных инициатив. "
              "Проект «1000/1000» предполагает участие 1000 спонсоров, каждый из которых вносит вклад от 1000 сомов и выше в развитие библиотеки.",
}

# 🔹 Тексты для FAQ
FAQ_TEXT = {
    "faq_1": "💸 **[KG] Кантип төлөөгө болот?**\n\n"
             "Төлөм жүргүзүү үчүн 'Реквизиттер' бөлүмүнө өтүңүз же администратордон сураңыз.\n\n"
             "**[RU] Как оплатить?**\n\n"
             "Перейдите в топик 'Реквизиты' или спросите у администратора.",

    "faq_2": "🔓 **[KG] Кандайча кирүүгө болот?**\n\n"
             "Төлөгөндөн кийин администраторго жазыңыз — ал тастыктап, кирүү мүмкүнчүлүгүн берет.\n\n"
             "**[RU] Как получить доступ?**\n\n"
             "После оплаты напишите администратору — он подтвердит и откроет доступ.",

    "faq_3": "❤️ **[KG] Кантип колдосо болот?**\n\n"
             "Ар ай сайын 1000 сом же андан көп өлчөмдө демөөрчүлүк жардам бере аласыз.\n\n"
             "**[RU] Как поддержать проект?**\n\n"
             "Вы можете ежемесячно вносить 1000 сом или больше в фонд библиотеки."
}
FAQ_TEXT = {
    "faq_1": "💸 **[KG] Кантип төлөөгө болот?**\n\n"
             "Төлөм жүргүзүү үчүн 'Реквизиттер' бөлүмүнө өтүңүз же администратордон сураңыз.\n\n"
             "**[RU] Как оплатить?**\n\n"
             "Перейдите в топик 'Реквизиты' или спросите у администратора.",

    "faq_2": "🔓 **[KG] Кандайча кирүүгө болот?**\n\n"
             "Төлөгөндөн кийин администраторго жазыңыз — ал тастыктап, кирүү мүмкүнчүлүгүн берет.\n\n"
             "**[RU] Как получить доступ?**\n\n"
             "После оплаты напишите администратору — он подтвердит и откроет доступ.",

    "faq_3": "❤️ **[KG] Кантип колдосо болот?**\n\n"
             "Ар ай сайын 1000 сом же андан көп өлчөмдө демөөрчүлүк жардам бере аласыз.\n\n"
             "**[RU] Как поддержать проект?**\n\n"
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
