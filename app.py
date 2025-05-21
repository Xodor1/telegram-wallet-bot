from flask import Flask, send_from_directory
from wallet_bot import start_bot
import threading
import os

app = Flask(__name__, static_folder="miniapp")

# Старт Telegram-бота в отдельном потоке
def run_bot():
    try:
        start_bot()
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")

# Основная страница miniapp (если нужно)
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

# Обслуживание всех остальных статических файлов (CSS, JS, изображения)
@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # Запускаем Telegram-бота в фоне
    threading.Thread(target=run_bot).start()

    # Запускаем Flask-сервер
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    
