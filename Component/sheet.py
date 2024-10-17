import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1e8py2FmqDJYPLrlr-DHwXm-g1iucPx3a8DX8bmVS0Gs/edit#gid=0')
worksheet = sheet.get_worksheet(0)

# ฟังก์ชันบันทึกข้อมูลลง Google Sheets
def add_GR_Data(name, GR_value):
    worksheet.append_row([name, GR_value,4])
