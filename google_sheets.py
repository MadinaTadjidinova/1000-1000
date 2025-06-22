import os
import json
import gspread
from google.oauth2.service_account import Credentials

# Настройка доступа
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_data = json.loads(os.getenv("GOOGLE_CREDENTIALS_JSON"))  # 🔐 читаем из переменной среды
credentials = Credentials.from_service_account_info(creds_data, scopes=scope)
client = gspread.authorize(credentials)

SPREADSHEET_NAME = "1000x1000-отчеты"
worksheet = client.open(SPREADSHEET_NAME).sheet1

def get_current_members():
    try:
        return int(worksheet.acell('A2').value)
    except:
        return 0

def get_raised_amount():
    try:
        return int(worksheet.acell('B2').value)
    except:
        return 0

def get_report_data():
    try:
        members = int(worksheet.acell('B1').value)
        goal = int(worksheet.acell('B2').value)
        amount = int(worksheet.acell('B3').value)
        return members, goal, amount
    except:
        return 0, 0, 0
