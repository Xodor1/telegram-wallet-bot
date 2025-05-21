from telebot import TeleBot, types
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    wallet_btn = types.KeyboardButton("💼 Кошелёк", web_app=types.WebAppInfo(url="https://your-webapp-url.com"))
    markup.add(wallet_btn)

    bot.send_message(
        message.chat.id,
        "✅ Бот работает! Нажми «Кошелёк», чтобы начать.",
        reply_markup=markup
    )

import flask

server = flask.Flask(__name__)

@server.route("/")
def home():
    return "Bot is alive!"

if __name__ == "__main__":
    import threading
    threading.Thread(target=bot.infinity_polling).start()
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
