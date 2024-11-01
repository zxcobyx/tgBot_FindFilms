import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Bot
from telegram.ext import Application, CommandHandler
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from transmission_rpc import Client
from functions import find_torrent as ft
from constants import BOT_TOKEN

# Настройки
# hash passwd - {e6910845aabe48f8b09deb053988e792e93c44ec}
transmission_client = Client(host='localhost', port=9091, username='transmission', password='YourName102')
TORRENT_FOLDER = '/home/cobyx/torrents'

async def start (update, context):
    await update.message.reply_text("Привет! Я бот.")

# Загрузка и отслеживание
def download_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    magnet_link = query.data.split('_')[1]
    torrent_id = transmission_client.add_torrent(magnet_link, download_dir=TORRENT_FOLDER).id
    query.answer()
    query.edit_message_text(text="Загрузка началась. Используйте /status для проверки статуса.")

def status(update: Update, context: CallbackContext) -> None:
    torrent_id = context.args[0]
    torrent = transmission_client.get_torrent(torrent_id)
    update.message.reply_text(f"Статус: {torrent.progress}% | Скорость: {torrent.rateDownload} кБ/с")

# Основной процесс
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("find", ft.find_torrent))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CallbackQueryHandler(download_callback, pattern='^download_'))
    application.run_polling()

if __name__ == '__main__':
    main()
