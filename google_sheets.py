import logging
import gspread
from google.oauth2.service_account import Credentials

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 🔹 Подключаемся к Google Sheets
SHEET_ID = "1pFCN-Ca0hiquICvEbSHndymcNCOyosjjZ624_ZYOkzc"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

# ✅ Функция записи платежей
def add_payment(user_id, username, amount, method, status="Ожидание"):
    from datetime import datetime
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    sheet.append_row([date, username, user_id, amount, method, status])

# ✅ Функция обновления статуса платежа
def update_payment_status(user_id, amount, status):
    logging.info(f"🔍 update_payment_status вызван с user_id={user_id}, amount={amount}, status={status}")

    # Получаем все данные из таблицы
    values = sheet.get_all_values()

    # Преобразуем сумму в строку для точного сравнения
    amount_str = str(amount).strip()

    last_matching_row = None  # Сюда запомним индекс последней найденной строки

    for i, row in enumerate(values):
        if len(row) < 6:  # Пропускаем пустые строки
            continue

        sheet_user_id = row[2].strip()
        sheet_amount = row[3].strip()

        # Проверяем соответствие user_id и суммы
        if sheet_user_id == str(user_id) and sheet_amount == amount_str:
            last_matching_row = i + 1  # Запоминаем последнюю найденную строку

    if last_matching_row:
        logging.info(f"✅ Найден последний платеж (строка {last_matching_row})! Обновляем статус на {status}")
        sheet.update_cell(last_matching_row, 6, status)  # Обновляем статус в 6-й колонке
        return True

    logging.info(f"❌ Платеж с user_id={user_id} и amount={amount} не найден!")
    return False