from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_admin_buttons(check_id):
    """Создаёт inline-кнопки для подтверждения/отклонения чека"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"confirm|{check_id}")],
            [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject|{check_id}")]
        ]
    )

def get_reports_keyboard():
    """Кнопки для выбора отчетов"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Отчет мероприятий", callback_data="show_events_report")],
            [InlineKeyboardButton(text="💰 Финансовый отчет", callback_data="show_finance_report")]
        ]
    )
