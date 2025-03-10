from flask import Flask, jsonify
from flask_cors import CORS
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

app = Flask(__name__)
CORS(app)  # 解決跨域問題，讓前端網頁能向此 API 發送請求

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

def get_google_docs_content(doc_id):
    """抓取指定 Google Docs 的內容並回傳 Python 字典。"""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('docs', 'v1', credentials=creds)
    document = service.documents().get(documentId=doc_id).execute()
    
    return document

@app.route('/api/docs/<doc_id>', methods=['GET'])
def get_docs_api(doc_id):
    """API 路由：提供指定 doc_id 文件的內容 (JSON 格式)。"""
    document = get_google_docs_content(doc_id)
    return jsonify(document)

if __name__ == '__main__':
    # 啟動 Flask 伺服器，預設在 http://127.0.0.1:5000/
    app.run(debug=True)
