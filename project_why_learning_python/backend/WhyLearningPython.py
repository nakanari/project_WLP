# WhyLearningPython.py

# 引入 Flask 模組與 jsonify 函式，用於建立 Web 伺服器並回傳 JSON 資料
from flask import Flask, jsonify
# 引入 Flask-CORS 模組，解決跨域問題，讓前端可以順利存取 API
from flask_cors import CORS

# 建立 Flask 應用程式實例
app = Flask(__name__)
# 啟用跨域資源共享 (CORS)，允許來自不同網域的請求
CORS(app)

# 定義一個 GET 路由 '/api/data'
@app.route('/api/data', methods=['GET'])
def get_data():
    # 模擬從 Google Docs 取得的文件資料
    data = {
        "documents": [
            {"id": 1, "title": "Document 1", "content": "This is document 1."},
            {"id": 2, "title": "Document 2", "content": "This is document 2."}
        ]
    }
    # 將 Python 字典轉換為 JSON 格式並回傳
    return jsonify(data)

# 檢查是否直接執行此檔案
if __name__ == '__main__':
    # 啟動 Flask 伺服器，debug 模式開啟方便開發除錯
    app.run(debug=True)
