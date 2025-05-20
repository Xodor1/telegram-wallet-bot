import telebot
import os
from flask import Flask, request

TOKEN = os.getenv("TELEGRAM_API_KEY")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
WEBHOOK_PATH = f"/{TOKEN}/"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Unsupported Media Type', 415

from telebot import types

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("💼 Кошелёк"),
        types.KeyboardButton("💱 Конвертация"),
        types.KeyboardButton("📊 Курс"),
        types.KeyboardButton("📰 Инфо-центр")
    )
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Выберите действие:",
        reply_markup=markup
    )
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
