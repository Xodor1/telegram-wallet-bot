import os
from flask import Flask, request, send_from_directory
import requests

# === Flask app ===
app = Flask(__name__, static_folder="miniapp")

# === Telegram bot config ===
BOT_TOKEN = "7987309610:AAHJkAlbPTxhToO9iyNvnh6I43kacWSP81M"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# === Serve frontend ===
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# === Telegram webhook endpoint ===
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = request.get_json()

    # Проверка наличия сообщения
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        # Пример: просто отвечаем тем же текстом
        reply_text = f"Вы написали: {text}"

        # Отправка ответа обратно в Telegram
        requests.post(TELEGRAM_API_URL, json={
            "chat_id": chat_id,
            "text": reply_text
        })

    return "OK", 200

# === Run server ===
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
