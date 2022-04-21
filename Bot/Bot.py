"""
.. module:: Bot
    :platform: Any
    :synopsis: Module for interraction with Telegram bot

"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


token = '5175481555:AAEp0UQJs1nWZxFQonsFvHDktGfHPZewwq0'


def start(update, context):
    """
    Обработка кнопки "Старт" в чате с ботом
    """
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text="Привет, я крипто бот")
    
updater = Updater(token, use_context=True)

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))

updater.start_polling()
updater.idle()
