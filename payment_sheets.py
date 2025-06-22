import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("payment_credentials.json", scope)
client = gspread.authorize(creds)

SPREADSHEET_NAME = "проект 1000*1000"
worksheet = client.open(SPREADSHEET_NAME).sheet1

def add_payment(user_id, username, amount, method, status):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    worksheet.append_row([  # добавляем в конец
        date, username, str(user_id), int(amount), method, status
    ])

def update_payment_status(user_id, amount, new_status):
    records = worksheet.get_all_records()
    for idx, row in enumerate(records, start=2):  # начинаем с 2, потому что первая строка — заголовки
        if str(row["Telegram ID"]) == str(user_id) and str(row["Сумма"]) == str(amount):
            worksheet.update_cell(idx, 6, new_status)  # 6-я колонка — статус
            break

