import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ContextTypes
from functions.find_torrent import find_torrent
from functions.torrent_utils import add_torrent_by_url, get_torrents_status, add_torrent_by_url_wn

class States:
    WAITING_FOR_TORRENT_QUERY = 1
    WAITING_FOR_TORRENT_NAME = 2
    WAITING_FOR_TORRENT_NAME_OLD = 3

async def start(update: Update, context: CallbackContext) -> None:
    """Отправляем приветственное сообщение и отображаем кнопки."""
    user = update.effective_user
    keyboard = [
        [
            InlineKeyboardButton("🔍 Найти торрент", callback_data='find_trnt'),
            InlineKeyboardButton("📊 Статус", callback_data='status')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Привет, {user.mention_html()}!",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def start_callback(update: Update, context: CallbackContext) -> None:
    """Отправляем приветственное сообщение и отображаем кнопки."""
    user = update.effective_user
    keyboard = [
        [
            InlineKeyboardButton("🔍 Найти торрент", callback_data='find_trnt'),
            InlineKeyboardButton("📊 Статус", callback_data='status')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.edit_message_text(
        f"Привет, {user.mention_html()}!",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def find_trnt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("⬅ Назад", callback_data='back_to_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.edit_message_text(
        text="Что вы хотите найти?\nНапишите в чат название, или нажмите кнопку ⬅ Назад",
        reply_markup=reply_markup
    )

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

            keyboard = [
                [InlineKeyboardButton("⬅ Назад", callback_data='back_to_start')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                text=f"Торрент был успешно загружен под именем '{new_name}'.",
                reply_markup=reply_markup
            )
        except Exception as e:
            keyboard = [
                [InlineKeyboardButton("⬅ Назад", callback_data='back_to_start')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                text="Произошла ошибка при добавлении торрента.",
                reply_markup=reply_markup
            )
        
        # Сбрасываем состояние после обработки имени
        context.user_data['state'] = None

async def download(update: Update, context: CallbackContext) -> None:
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
        '''
        Добавить кнопку, которая оставит текущее название торрента (стоковое)
        '''
        keyboard = [
            [InlineKeyboardButton("💾 Оставить текущее название", callback_data='keep_current_name')]        
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="Как вы хотите назвать торрент?",
            reply_markup=reply_markup
        )
        
        # Устанавливаем состояние ожидания имени
        context.user_data['state'] = States.WAITING_FOR_TORRENT_NAME
    else:
        await query.edit_message_text("Ошибка: неверный формат данных.")
        return

'''
Добавить кнопку Обновить статус загрузки в статусе загружающихся торрентов
'''
async def status(update: Update, context: CallbackContext) -> None:
    """Получаем статус всех загружающихся торрентов."""
    torrents_status = get_torrents_status()
    
    if torrents_status is None or len(torrents_status) == 0:
        await update.callback_query.answer()  # Подтверждение нажатия
        keyboard = [
            [InlineKeyboardButton("⬅ Назад", callback_data='back_to_start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.callback_query.edit_message_text(
            text="Нет активных торрентов для загрузки.",
            reply_markup=reply_markup
        )
        return

    # Формируем сообщение со статусом каждого торрента
    message = "Статус загружающихся торрентов:\n"
    for i, torrent in enumerate(torrents_status, 1):
        message += f"{i}: {torrent['name']}\n"
        message += f"   Прогресс: {torrent['progress']:.1f}%\n\n"
    
    await update.callback_query.answer()  # Подтверждение нажатия

    keyboard_ = [
        [InlineKeyboardButton("⬅ Назад", callback_data='back_to_start')]
    ]
    reply_markup_ = InlineKeyboardMarkup(keyboard_)

    await update.callback_query.edit_message_text(
        message,
        reply_markup=reply_markup_
    )

async def keep_current_name(update: Update, context: CallbackContext) -> None:
    torrent_url = context.user_data.get('torrent_url')
    try:
        # Загружаем торрент по URL с новым именем
        await add_torrent_by_url_wn(torrent_url)

        keyboard = [
            [InlineKeyboardButton("⬅ Назад", callback_data='back_to_start')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.callback_query.edit_message_text(
            text=f"Торрент был успешно загружен под стандартным именем.",
            reply_markup=reply_markup
        )
    except Exception as e:
        keyboard = [
                [InlineKeyboardButton("⬅ Назад", callback_data='back_to_start')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            text="Произошла ошибка при добавлении торрента.",
            reply_markup=reply_markup
        )