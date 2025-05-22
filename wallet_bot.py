import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from mnemonic import Mnemonic
import csv

ADMIN_ID = 6871170832  # ← Укажи свой Telegram ID

def generate_wallet():
    mnemo = Mnemonic("english")
    seed_phrase = mnemo.generate(strength=128)
    return seed_phrase

def save_user(user_id, seed_phrase):
    file = "users.csv"
    account_id = "id1"
    if os.path.exists(file):
        with open(file, "r") as f:
            existing = list(csv.reader(f))
            account_id = f"id{len(existing) + 1}"
    with open(file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([user_id, account_id, seed_phrase, "private_key_placeholder"])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    seed_phrase = generate_wallet()
    save_user(user_id, seed_phrase)
    await update.message.reply_text(f"Ваш seed:\n{seed_phrase}")

def start_bot(token: str, webhook_url: str):
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        webhook_url=webhook_url,
        webhook_path=os.environ.get("WEBHOOK_PATH", "")
    )
