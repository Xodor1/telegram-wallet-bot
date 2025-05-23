import os
from wallet_bot import start_bot

if __name__ == '__main__':
    token = os.environ.get("TELEGRAM_BOT_TOKEN") or "YOUR_REAL_TELEGRAM_BOT_TOKEN"
    webhook_path = os.environ.get("WEBHOOK_PATH") or "bot-hook"
    render_url = os.environ.get("RENDER_EXTERNAL_URL") or "https://telegram-wallet-bot-2lyl.onrender.com"
    webhook_url = f"{render_url}/{webhook_path}"
    start_bot(token, webhook_url)
