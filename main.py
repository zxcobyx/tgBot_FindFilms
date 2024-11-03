import re
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters, ContextTypes
from functions.find_torrent import find_torrent
from constants import BOT_TOKEN
from functions.torrent_utils import add_torrent_by_url, get_torrents_status

class States:
    WAITING_FOR_TORRENT_QUERY = 1
    WAITING_FOR_TORRENT_NAME = 2

async def start(update: Update, context: CallbackContext) -> None:
    """Отправляем приветственное сообщение и отображаем кнопки."""
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.mention_html()}! Добро пожаловать в бота.",
        reply_markup=ReplyKeyboardMarkup(
            [['Найти торрент', 'Статус']],  # Названия кнопок в одной строке
            one_time_keyboard=True,  # Скрыть клавиатуру после выбора
            resize_keyboard=True  # Изменить размер клавиатуры для соответствия кнопкам
        ),
        parse_mode='HTML'
    )

async def find_trnt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Что вы хотите найти?")
    # Устанавливаем состояние ожидания ответа от пользователя
    context.user_data['state'] = States.WAITING_FOR_TORRENT_QUERY

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Обработка сообщений от пользователей."""
    text = update.message.text

    # Проверяем состояние ожидания запроса на торрент
    if context.user_data.get('state') == States.WAITING_FOR_TORRENT_QUERY:
        user_query = text
        await find_torrent(update, user_query)
        context.user_data['state'] = None  # Сбрасываем состояние

    elif context.user_data.get('state') == States.WAITING_FOR_TORRENT_NAME:
        new_name = text
        torrent_url = context.user_data.get('torrent_url')
        
        try:
            # Загружаем торрент по URL с новым именем
            await add_torrent_by_url(torrent_url, new_name=new_name)

            await update.message.reply_text(
                text=f"Торрент был успешно загружен под именем '{new_name}'."
            )
        except Exception as e:
            await update.message.reply_text(
                text="Произошла ошибка при добавлении торрента."
            )
        
        # Сбрасываем состояние после обработки имени
        context.user_data['state'] = None

    elif text == 'Найти торрент':
        await find_trnt(update, context)

    elif text == 'Статус':
        await status(update, context)

async def download_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    # Извлекаем URL из callback_data
    match = re.match(r'download_(\d+)_(.*)', query.data)
    if match:
        index = match.group(1)
        torrent_url = match.group(2)
        
        if not torrent_url.startswith(('http://', 'https://')):
            torrent_url = 'https://' + torrent_url.lstrip('/')

        # Сохраняем информацию о торренте в контексте
        context.user_data['torrent_url'] = torrent_url
        context.user_data['torrent_index'] = index
        
        # Запрашиваем у пользователя новое имя для торрента
        await query.edit_message_text(
            text="Как вы хотите назвать торрент?"
        )
        
        # Устанавливаем состояние ожидания имени
        context.user_data['state'] = States.WAITING_FOR_TORRENT_NAME
    else:
        await query.edit_message_text("Ошибка: неверный формат данных.")
        return

async def status(update: Update, context: CallbackContext) -> None:
    """Получаем статус всех загружающихся торрентов."""
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
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(download_callback, pattern='^download_'))
    application.run_polling()

if __name__ == '__main__':
    main()