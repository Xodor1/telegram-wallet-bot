from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from mnemonic import Mnemonic
import csv
import os

TELEGRAM_BOT_TOKEN = "7987309610:AAHJkAlbPTxhToO9iyNvnh6I43kacWSP81M"  # ← Вставь сюда свой токен
ADMIN_ID = 123456789               # ← Вставь свой Telegram ID

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

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    seed_phrase = generate_wallet()
    save_user(user_id, seed_phrase)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Ваш seed:\n{seed_phrase}"
    )

def start_bot():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()
