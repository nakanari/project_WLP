import json
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_google_sheet_data(json_keyfile_path, spreadsheet_url, sheet_name=None):
    """
    下載指定 Google Sheet 資料並轉換為字典格式。
    """
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
    gc = gspread.authorize(credentials)

    # 開啟 Google Sheet
    spreadsheet = gc.open_by_url(spreadsheet_url)
    worksheet = spreadsheet.worksheet(sheet_name) if sheet_name else spreadsheet.get_worksheet(0)

    # 取得所有數據
    data = worksheet.get_all_values()
    
    # 轉換為 DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    df.replace('', pd.NA, inplace=True)
    df.dropna(how='all', inplace=True)  # 移除全為 NaN 的列

    # 轉換 NaN 為 None
    df = df.where(pd.notna(df), None)

    return df.to_dict(orient='records')

# 設定 Google Service 帳戶金鑰路徑與 Google Sheet URL
json_keyfile_path = 'C:/Users/lovel/Documents/Code_demo/VS_Code/test/sheet.json'
sheet_url = 'https://docs.google.com/spreadsheets/d/1uQPoH6WLKYsEQ-VwmhY3Tf1SJqsekHIPNMe8tuLwLeI/edit?gid=0#gid=0'

# 下載並轉換資料
data = load_google_sheet_data(json_keyfile_path, sheet_url)

# 輸出結果
print(json.dumps(data, indent=4, ensure_ascii=False))