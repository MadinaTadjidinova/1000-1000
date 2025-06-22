import os
import json
import gspread
from google.oauth2.service_account import Credentials
import pytz
from datetime import datetime
import uuid

# Настройка доступа
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_data = json.loads(os.getenv("PAYMENT_CREDENTIALS_JSON"))  # 🔐 читаем из переменной среды
credentials = Credentials.from_service_account_info(creds_data, scopes=scope)
client = gspread.authorize(credentials)

SPREADSHEET_NAME = "проект 1000*1000"
worksheet = client.open(SPREADSHEET_NAME).sheet1

def add_payment(user_id, username, amount, method, status):
    tz = pytz.timezone('Asia/Bishkek')
    date = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
    check_id = str(uuid.uuid4())[:8]
    worksheet.append_row([
        check_id, date, username, str(user_id), int(amount), method, status
    ])
    return check_id

def update_payment_status_by_id(check_id, new_status):
    expected_headers = ["ID чека", "Дата", "Имя пользователя", "Telegram ID", "Сумма", "Способ оплаты", "Статус"]
    records = worksheet.get_all_records(expected_headers=expected_headers)
    for idx, row in enumerate(records, start=2):
        if str(row["ID чека"]) == str(check_id):
            worksheet.update_cell(idx, 7, new_status)
            break
