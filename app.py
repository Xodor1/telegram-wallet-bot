from flask import Flask
from wallet_bot import start_bot
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running with webhook."

if __name__ == '__main__':
    # Telegram bot token
    token = os.environ.get("TELEGRAM_BOT_TOKEN") or "YOUR_ACTUAL_TELEGRAM_BOT_TOKEN"
    
    # Webhook path — произвольно, но должно совпадать с тем, что ты укажешь в Telegram
    webhook_path = os.environ.get("WEBHOOK_PATH") or "bot-hook"
    
    # Render external URL
    render_url = os.environ.get("RENDER_EXTERNAL_URL") or "https://telegram-wallet-bot-2lyl.onrender.com"
    
    if not token:
        raise Exception("TELEGRAM_BOT_TOKEN is not set")

    # Полный webhook
    webhook_url = f"{render_url}/{webhook_path}"
    
    # Запуск бота
    start_bot(token, webhook_url)
