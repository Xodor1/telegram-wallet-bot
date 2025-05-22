from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
from mnemonic import Mnemonic
import csv
import os
from flask import request

ADMIN_ID = 123456789  # ← твой Telegram ID

# Генерация сид-фразы
def generate_wallet():
    mnemo = Mnemonic("english")
    seed_phrase = mnemo.generate(strength=128)
    return seed_phrase

# Сохранение пользователя
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

# Обработка команды /start
def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    seed_phrase = generate_wallet()
    save_user(user_id, seed_phrase)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Ваш seed:\n{seed_phrase}"
    )

# Основная функция запуска бота через Webhook
def setup_dispatcher(bot: Bot):
    dp = Dispatcher(bot, None, workers=0, use_context=True)
    dp.add_handler(CommandHandler("start", start))
    return dp

# Flask endpoint, вызываемый Telegram при новых событиях
def webhook_handler(app, bot_token, webhook_url_path):
    bot = Bot(bot_token)
    dp = setup_dispatcher(bot)

    @app.route(f"/{webhook_url_path}", methods=["POST"])
    def webhook():
        if request.method == "POST":
            update = Update.de_json(request.get_json(force=True), bot)
            dp.process_update(update)
            return "ok", 200
