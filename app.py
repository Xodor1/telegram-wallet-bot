from flask import Flask
from wallet_bot import start_bot
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running with webhook."

if __name__ == '__main__':
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    webhook_path = os.environ.get("WEBHOOK_PATH")
    if not token or not webhook_path:
        raise Exception("Токен или webhook path не установлены")

    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    if not render_url:
        render_url = "https://your_render_domain.onrender.com"  # ← Заменишь вручную, если нужно

    webhook_url = f"{render_url}/{webhook_path}"
    start_bot(token, webhook_url)
