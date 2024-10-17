import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ฟังก์ชันเชื่อมต่อกับ Google Sheets
def connect_to_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1e8py2FmqDJYPLrlr-DHwXm-g1iucPx3a8DX8bmVS0Gs/edit#gid=0')
    worksheet = sheet.get_worksheet(0)
    return worksheet

# ฟังก์ชันบันทึกหรืออัปเดตข้อมูล (เริ่มจากแถวที่ 4 เป็นต้นไป)
def add_GR_Data(name, GR_value):
    worksheet = connect_to_google_sheets()

    cell = worksheet.find(name, in_column=1)
    
    if cell and cell.row >= 4:
        row_number = cell.row
        worksheet.update(f'B{row_number}', GR_value)
    else:
        row_number = 4
        while worksheet.cell(row_number, 1).value:
            row_number += 1

        worksheet.update(f'A{row_number}', name)
        worksheet.update(f'B{row_number}', GR_value)
