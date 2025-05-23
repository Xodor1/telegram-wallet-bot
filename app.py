from flask import Flask, request
from wallet_bot import start_bot
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running with webhook."

if __name__ == '__main__':
    # Получаем токен и путь webhook из переменных окружения
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    webhook_path = os.environ.get("WEBHOOK_PATH")

    if not token or not webhook_path:
        raise Exception("Токен (TELEGRAM_BOT_TOKEN) или путь webhook (WEBHOOK_PATH) не установлены")

    # Получаем внешний URL Render
    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    if not render_url:
        render_url = "https://your-render-domain.onrender.com"  # Замени вручную если нужно

    webhook_url = f"{render_url}/{webhook_path}"

    # Стартуем Telegram-бота
    start_bot(token, webhook_url)

    # Запускаем Flask-сервер
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
