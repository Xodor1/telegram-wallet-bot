from flask import Flask, send_from_directory
from wallet_bot import webhook_handler
import os

app = Flask(__name__, static_folder="miniapp")

# Статические файлы
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # Получаем токен и путь webhook
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    webhook_path = os.environ.get("WEBHOOK_PATH", "webhook")  # Например, "mybotwebhook123"

    if not telegram_token:
        raise Exception("TELEGRAM_BOT_TOKEN не установлен")

    # Запускаем Webhook-хендлер
    webhook_handler(app, telegram_token, webhook_path)

    # Запуск Flask-сервера
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
