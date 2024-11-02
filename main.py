import re
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from functions import find_torrent as ft
from constants import BOT_TOKEN
from functions.torrent_utils import download_torrent_file, add_torrent, get_torrent_status

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
        # Загружаем торрент-файл
        torrent_content = await download_torrent_file(torrent_url)
        if torrent_content:
            # Добавляем торрент
            torrent_id = await add_torrent(torrent_content)
            await query.edit_message_text(
                text=f"Загрузка торрента {index} началась. ID торрента: {torrent_id}. "
                     f"Используйте /status {torrent_id} для проверки статуса."
            )
        else:
            await query.edit_message_text("Не удалось загрузить торрент-файл.")
    except Exception as e:
        await query.edit_message_text(
            text=f"Произошла ошибка при добавлении торрента: {str(e)}"
        )

async def status(update: Update, context: CallbackContext) -> None:
    if not context.args:
        await update.message.reply_text("Пожалуйста, укажите ID торрента.")
        return

    torrent_id = int(context.args[0])
    status = get_torrent_status(torrent_id)
    await update.message.reply_text(f"Статус торрента {torrent_id}: {status['progress']}% | Скорость: {status['rateDownload']:.2f} кБ/с")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("find", ft.find_torrent))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CallbackQueryHandler(download_callback, pattern='^download_'))
    application.run_polling()

if __name__ == '__main__':
    main()