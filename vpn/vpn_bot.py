import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import sqlite3

# Вставьте ваш токен
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Подключение к базе данных
conn = sqlite3.connect('vpn_users.db')
c = conn.cursor()

# Создание таблицы пользователей
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, plan TEXT)''')
conn.commit()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот для выдачи ключей VPN. Используйте команду /register для регистрации.')

def register(update: Update, context: CallbackContext) -> None:
    username = update.message.from_user.username
    c.execute("INSERT INTO users (username, plan) VALUES (?, ?)", (username, 'basic'))
    conn.commit()
    update.message.reply_text('Вы успешно зарегистрированы! Используйте команду /pay для оплаты.')

def pay(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Перейдите по ссылке для оплаты: [Ссылка на платежную систему]')

def issue_key(update: Update, context: CallbackContext) -> None:
    username = update.message.from_user.username
    c.execute("SELECT plan FROM users WHERE username=?", (username,))
    user = c.fetchone()
    
    if user:
        plan = user[0]
        # Генерация ключа в зависимости от плана
        key = generate_key(plan)
        update.message.reply_text(f'Ваш ключ для подключения к VPN: {key}')
    else:
        update.message.reply_text('Вы не зарегистрированы. Используйте команду /register.')

def generate_key(plan):
    # Здесь реализуйте логику генерации ключа для OpenVPN или WireGuard
    return "generated_key_based_on_plan"

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("register", register))
    dispatcher.add_handler(CommandHandler("pay", pay))
    dispatcher.add_handler(CommandHandler("getkey", issue_key))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

Найти еще