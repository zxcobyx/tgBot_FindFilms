from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from functions.find_torrent import find_torrent
from functions.callback import start, handle_message, download, find_trnt, status, start_callback, keep_current_name
from constants import BOT_TOKEN

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.add_handler(CallbackQueryHandler(download, pattern='^download_'))
    application.add_handler(CallbackQueryHandler(find_torrent, pattern='^find_torrent$'))
    application.add_handler(CallbackQueryHandler(find_trnt, pattern='^find_trnt$'))
    application.add_handler(CallbackQueryHandler(status, pattern='^status$'))
    application.add_handler(CallbackQueryHandler(start_callback, pattern='^back_to_start$'))
    application.add_handler(CallbackQueryHandler(keep_current_name, pattern='^keep_current_name$'))

    application.run_polling()

if __name__ == '__main__':
    main()