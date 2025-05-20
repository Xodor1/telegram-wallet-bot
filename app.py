import telebot
from telebot import types
from mnemonic import Mnemonic
import time

TOKEN = 7987309610:AAHJkAlbPTxhToO9iyNvnh6I43kacWSP81M # 🔁 Вставь сюда свой токен

bot = telebot.TeleBot(TOKEN)

# Сохраняем временные данные пользователей
user_data = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("💼 Кошелёк"))
    bot.send_message(message.chat.id, "✅ Бот работает! Нажми «Кошелёк», чтобы начать.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "💼 Кошелёк")
def wallet_menu(message):
    chat_id = message.chat.id

    # Имитация загрузки
    msg = bot.send_message(chat_id, "⏳ Загружаю кошелёк...")
    time.sleep(2)
    bot.edit_message_text("✅ Кошелёк готов!", chat_id, msg.message_id)

    # Генерация сид-фразы
    mnemo = Mnemonic("english")
    seed_phrase = mnemo.generate(strength=128)  # 12 слов
    seed_words = seed_phrase.split()
    user_data[chat_id] = {
        "seed_phrase": seed_phrase,
        "words": seed_words
    }

    # Отправляем сид-фразу
    bot.send_message(chat_id, f"💡 Это ваша сид-фраза:\n\n<code>{seed_phrase}</code>\n\nСкопируйте и сохраните в надёжном месте!", parse_mode="HTML")

    # Запрос подтверждения 3 слов
    bot.send_message(chat_id, "Для подтверждения, введите 7-е слово из вашей сид-фразы:")
    bot.register_next_step_handler(message, lambda m: confirm_word(m, position=6))  # 7-е слово (index 6)

def confirm_word(message, position):
    chat_id = message.chat.id
    word = message.text.strip().lower()

    if user_data.get(chat_id) is None or position >= len(user_data[chat_id]["words"]):
        bot.send_message(chat_id, "❌ Ошибка! Попробуйте заново нажать 'Кошелёк'.")
        return

    if user_data[chat_id]["words"][position] != word:
        bot.send_message(chat_id, "❌ Неверно! Попробуйте ещё раз.")
        bot.register_next_step_handler(message, lambda m: confirm_word(m, position=position))
        return

    if position == 6:
        bot.send_message(chat_id, "✅ Верно! Теперь введите 2-е слово:")
        bot.register_next_step_handler(message, lambda m: confirm_word(m, position=1))
    elif position == 1:
        bot.send_message(chat_id, "✅ Отлично! Теперь введите 11-е слово:")
        bot.register_next_step_handler(message, lambda m: confirm_word(m, position=10))
    elif position == 10:
        bot.send_message(chat_id, "✅ Подтверждение прошло успешно!")
        show_wallet_main_menu(message)

def show_wallet_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("💰 Баланс"),
        types.KeyboardButton("➕ Пополнить"),
        types.KeyboardButton("🔁 Перевести"),
    )
    markup.add(
        types.KeyboardButton("📥 Вывод"),
        types.KeyboardButton("🔄 Обмен"),
        types.KeyboardButton("🧾 История")
    )

    bot.send_message(message.chat.id, "Вы вошли в кошелёк. Выберите действие:", reply_markup=markup)

# 🔁 Обмен (заглушка)
@bot.message_handler(func=lambda message: message.text == "🔄 Обмен")
def exchange_crypto(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    tokens = ["BTC", "ETH", "BNB", "SOL", "TRX", "TON", "LTC"]
    for token in tokens:
        markup.add(types.KeyboardButton(token))
    markup.add(types.KeyboardButton("🔙 Назад"))
    bot.send_message(message.chat.id, "Выберите валюту, в которую хотите обменять USDT:", reply_markup=markup)
    bot.register_next_step_handler(message, process_exchange_selection)

def process_exchange_selection(message):
    token = message.text.strip().upper()
    if token not in ["BTC", "ETH", "BNB", "SOL", "TRX", "TON", "LTC"]:
        bot.send_message(message.chat.id, "❌ Неверный выбор. Попробуйте снова.")
        return

    amount = 100
    discount = 4  # %
    final_amount = amount * (1 - discount / 100)

    bot.send_message(
        message.chat.id,
        f"💱 Обмен USDT → {token}\n"
        f"Сумма: {amount} USDT\n"
        f"Скидка: {discount}%\n"
        f"Вы получите: ~{round(final_amount, 2)} {token}"
    )

# Запуск бота (через polling)
if __name__ == '__main__':
    bot.infinity_polling()
