# backend.py

# --------------------------
# 匯入必要模組與套件
# --------------------------
from __future__ import print_function
import os.path
from flask import Flask, jsonify, request  # Flask 用於建立後端 API，jsonify 用於回傳 JSON，request 用於獲取查詢參數
from flask_cors import CORS             # Flask-CORS 用於解決跨域請求問題
from google.oauth2.credentials import Credentials  # 用於處理 OAuth2 憑證
from google_auth_oauthlib.flow import InstalledAppFlow  # 用於進行 OAuth2 驗證流程
from google.auth.transport.requests import Request  # 用於處理 HTTP 請求中的認證更新
from googleapiclient.discovery import build   # 用於建立 Google API 的服務物件

# --------------------------
# 定義 API 存取範圍 (Scopes)
# --------------------------
# DOC_SCOPES 用於 Google Docs API，只讀取文件內容
DOC_SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
# DRIVE_SCOPES 用於 Google Drive API，僅讀取文件的元資料（例如文件 ID 與名稱）
DRIVE_SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

# --------------------------
# 初始化 Flask 應用程式
# --------------------------
app = Flask(__name__)
CORS(app)  # 啟用跨域資源共享，允許前端從不同來源呼叫本 API

# --------------------------
# 函式：取得 Google Docs API 憑證
# --------------------------
def get_docs_credentials():
    """
    取得或更新 Google Docs API 所需的 OAuth2 憑證。
    憑證會儲存在 'token.json' 中，下次呼叫時會自動使用此檔案。
    """
    creds = None
    if os.path.exists('token.json'):
        # 從 token.json 讀取現有憑證
        creds = Credentials.from_authorized_user_file('token.json', DOC_SCOPES)
    # 若沒有有效的憑證，則進行授權流程
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # 若憑證過期且有 refresh_token，則自動刷新
            creds.refresh(Request())
        else:
            # 使用 credentials.json（從 Google Cloud Console 下載）來啟動授權流程
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', DOC_SCOPES)
            creds = flow.run_local_server(port=0)
        # 儲存取得的新憑證至 token.json 以供下次使用
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# --------------------------
# 函式：取得 Google Drive API 憑證
# --------------------------
def get_drive_credentials():
    """
    取得或更新 Google Drive API 所需的 OAuth2 憑證。
    憑證會儲存在 'token_drive.json' 中，下次呼叫時會自動使用此檔案。
    """
    creds = None
    if os.path.exists('token_drive.json'):
        creds = Credentials.from_authorized_user_file('token_drive.json', DRIVE_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', DRIVE_SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token_drive.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# --------------------------
# API 路由：取得 Google Docs 文件內容
# --------------------------
@app.route('/api/data', methods=['GET'])
def get_data():
    """
    此 API 用於取得 Google Docs 文件內容。
    用戶需在查詢字串中提供 'docId'（例如 /api/data?docId=YOUR_DOCUMENT_ID）。
    若成功，回傳 JSON 格式的文件標題與內容；否則回傳錯誤訊息。
    """
    # 從請求中獲取查詢參數 docId
    doc_id = request.args.get('docId')
    if not doc_id:
        # 當 docId 未提供時回傳錯誤
        return jsonify({'error': 'No document id provided. Please add ?docId=YOUR_DOCUMENT_ID to the URL.'}), 400

    # 取得 Google Docs API 憑證並建立服務物件
    creds = get_docs_credentials()
    service = build('docs', 'v1', credentials=creds)
    try:
        # 使用文件 ID 呼叫 API 取得文件內容
        document = service.documents().get(documentId=doc_id).execute()
    except Exception as e:
        # 捕獲並回傳任何 API 呼叫失敗的錯誤
        return jsonify({'error': str(e)}), 500

    # 取得文件的標題與內容（內容是文件主體的結構化資料）
    title = document.get('title')
    content = document.get('body').get('content')
    # 回傳 JSON 格式的文件資料
    return jsonify({
        'title': title,
        'content': content
    })

# --------------------------
# 函式：利用 Google Drive API 搜尋文件 ID
# --------------------------
def search_file_by_name(file_name: str):
    """
    根據傳入的檔案名稱使用 Google Drive API 搜尋文件，
    並回傳第一個匹配的文件 ID。
    
    :param file_name: 使用者輸入的檔案名稱（例如 "test.doc"）
    :return: 找到的文件 ID；若無匹配則返回 None
    """
    creds = get_drive_credentials()
    service = build('drive', 'v3', credentials=creds)
    # 建立搜尋查詢：這裡使用完全匹配條件；若需模糊搜尋可調整查詢運算符
    query = f"name = '{file_name}'"
    results = service.files().list(
        q=query,
        spaces='drive',
        fields="files(id, name)",
        pageSize=1
    ).execute()
    items = results.get('files', [])
    if not items:
        # 沒有找到匹配的文件
        return None
    else:
        # 回傳找到的第一個文件的 ID
        return items[0]['id']

# --------------------------
# API 路由：根據檔案名稱搜尋文件 ID
# --------------------------
@app.route('/api/search', methods=['GET'])
def search_file():
    """
    此 API 用於根據使用者提供的檔案名稱搜尋文件，
    並回傳第一個匹配文件的 ID。
    用戶需在查詢字串中提供 'fileName'（例如 /api/search?fileName=test.doc）。
    """
    file_name = request.args.get('fileName')
    if not file_name:
        return jsonify({'error': 'No file name provided. Please add ?fileName=YOUR_FILE_NAME to the URL.'}), 400

    file_id = search_file_by_name(file_name)
    if not file_id:
        return jsonify({'error': f'No file found with name: {file_name}'}), 404
    # 回傳文件名稱與找到的文件 ID
    return jsonify({'fileName': file_name, 'fileId': file_id})

# --------------------------
# 定義根路由（"/"），提供簡單的首頁訊息
# --------------------------
@app.route('/')
def index():
    """
    根路由，顯示簡單歡迎訊息，並提示可用的 API 路徑。
    """
    return ("Welcome to the Google Docs and Drive API backend! "
            "Use /api/data?docId=YOUR_DOCUMENT_ID to fetch document content, "
            "or /api/search?fileName=YOUR_FILE_NAME to search for a document ID.")

# --------------------------
# 啟動 Flask 伺服器
# --------------------------
if __name__ == '__main__':
    # 啟動伺服器，debug 模式開啟有助於開發時自動重新載入與錯誤訊息顯示
    app.run(debug=True)
