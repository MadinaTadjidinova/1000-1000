import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Настройка доступа
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

SPREADSHEET_NAME = "1000x1000-отчеты"
worksheet = client.open(SPREADSHEET_NAME).sheet1  # первый лист

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
