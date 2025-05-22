from flask import Flask, send_from_directory
from wallet_bot import start_bot
import threading
import os

app = Flask(__name__, static_folder="miniapp")

# Старт Telegram-бота в отдельном потоке
def run_bot():
    try:
        telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        if not telegram_token or not telegram_token.startswith(""):
            raise ValueError("TELEGRAM_BOT_TOKEN не установлен или некорректен.")
        
        start_bot(telegram_token)  # передаём токен в функцию бота
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")

# Основная страница miniapp
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

# Обслуживание всех остальных статических файлов
@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # Запускаем Telegram-бота в фоне
    threading.Thread(target=run_bot).start()

    # Запускаем Flask-сервер
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
