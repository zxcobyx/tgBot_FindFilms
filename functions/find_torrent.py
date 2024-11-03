from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from functions.rutor import search_torrent_rutor
from functions.rutracker import search_torrent_rutracker

async def find_torrent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    best_torrent_rutor = await search_torrent_rutor(context)

    if best_torrent_rutor:
        message = "Найдены лучшие торренты на Rutor:\n\n"
        button_row = []  # Одна строка для всех кнопок

        for i, torrent in enumerate(best_torrent_rutor, 1):
            message += f"{i}. {torrent['title']}\n"
            message += f"   Сиды: {torrent['seeds']}\n"
            message += f"   Размер: {torrent['size']}\n"
            message += f"   Ссылка: {torrent['link']}\n\n"

            button_row.append(InlineKeyboardButton(f"Скачать {i}", callback_data=f"download_{i}_{torrent['magnet_link']}"))

        keyboard = [
            button_row,
            [InlineKeyboardButton("⬅ Назад", callback_data='back_to_start')]    
        ]

        await update.message.reply_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text("Не удалось найти торренты по вашему запросу.")
    
    # best_torrent_rutracker = await search_torrent_rutracker(query)
    # if best_torrent_rutor:
    #     await update.message.reply_text(
    #         f"Найден торрент на Rutor: \n{best_torrent_rutor['title']}\nСиды: {best_torrent_rutor['seeds']}\nСсылка: {best_torrent_rutor['link']}",
    #         reply_markup=InlineKeyboardMarkup([
    #             [InlineKeyboardButton("Скачать", callback_data=f"download_{best_torrent_rutor['magnet_link']}")]
    #         ])
    #     )

    #     # await update.message.reply_text(
    #     #     f"Найден торрент на Rutracker: {best_torrent_rutracker['title']}\nСиды: {best_torrent_rutracker['seeds']}",
    #     #     reply_markup=InlineKeyboardMarkup([
    #     #         [InlineKeyboardButton("Скачать", callback_data=f"download_{best_torrent_rutracker['magnet_link']}")]
    #     #     ])
    #     # )
    # else:
    #     await update.message.reply_text("Не удалось найти торренты по вашему запросу.")