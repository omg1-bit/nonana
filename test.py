import requests
BOT_TOKEN = "8865223524:AAF-iaw7xF614IrEi1kxIYntSfPaccpN6-4"
CHAT_ID = "8130482893"
msg = "✅ البوت شغال وجاهز"
url = f"https://api.telegram.org/bot8865223524:AAF-iaw7xF614IrEi1kxIYntSfPaccpN6-4/sendMessage"
requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
