from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from functions.rutor import search_torrent_rutor
from functions.rutracker import search_torrent_rutracker
    
async def find_torrent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = " ".join(context.args)

    best_torrent_rutor = await search_torrent_rutor(query)  # Ожидаем результат функции поиска
    best_torrent_rutracker = await search_torrent_rutracker(query)

    if best_torrent_rutor or best_torrent_rutracker:
        # await update.message.reply_text(
        #     f"Найден торрент на Rutor: {best_torrent_rutor['title']}\nСиды: {best_torrent_rutor['seeds']}",
        #     reply_markup=InlineKeyboardMarkup([
        #         [InlineKeyboardButton("Скачать", callback_data=f"download_{best_torrent_rutor['magnet_link']}")]
        #     ])
        # )

        await update.message.reply_text(
            f"Найден торрент на Rutracker: {best_torrent_rutracker['title']}\nСиды: {best_torrent_rutracker['seeds']}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Скачать", callback_data=f"download_{best_torrent_rutracker['magnet_link']}")]
            ])
        )
    else:
        await update.message.reply_text("Не удалось найти торренты по вашему запросу.")