import re
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from functions import find_torrent as ft
from constants import BOT_TOKEN
from functions.torrent_utils import add_torrent_by_url, get_torrents_status

async def start(update, context):
    await update.message.reply_text("Привет! Я персональный бот для оптимизации и ускорения работы с медиафайлами. Я умею искать и загружать фильмы с таких торрент-трекеров, как Rutracker и Rutor. Надеюсь, вам понравится пользоваться мной.")

async def download_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    # Извлекаем URL из callback_data
    match = re.match(r'download_(\d+)_(.*)', query.data)
    if match:
        index = match.group(1)
        torrent_url = match.group(2)
    else:
        await query.edit_message_text("Ошибка: неверный формат данных.")
        return

    try:
        if not torrent_url.startswith(('http://', 'https://')):
            torrent_url = 'https://' + torrent_url.lstrip('/')

        # Загружаем торрент по URL
        await add_torrent_by_url(torrent_url)  # Передаем список с одним URL

        await query.edit_message_text(
            text=f"Загрузка торрента {index} началась. Используйте /status {index} для проверки статуса."
        )
    except Exception as e:
        await query.edit_message_text(
            text="Произошла ошибка при добавлении торрента"
        )

async def status(update: Update, context: CallbackContext) -> None:
    # Получаем статус всех загружающихся торрентов
    torrents_status = get_torrents_status()
    
    if torrents_status is None:
        await update.message.reply_text("Нет активных торрентов для загрузки.")
        return

    # Формируем сообщение со статусом каждого торрента
    message = "Статус загружающихся торрентов:\n"
    for i, torrent in enumerate(torrents_status, 1):
        message += f"{i}: {torrent['name']}\n"
        message += f"   Прогресс: {torrent['progress']:.1f}%\n\n"
    
    await update.message.reply_text(message)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("find", ft.find_torrent))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CallbackQueryHandler(download_callback, pattern='^download_'))
    application.run_polling()

if __name__ == '__main__':
    main()