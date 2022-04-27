"""This module contains an object that represents a Telegram Bot."""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


class Bot:
    """_summary_
    """
    
    token = '5175481555:AAEp0UQJs1nWZxFQonsFvHDktGfHPZewwq0'
    
    
    def __init__(self):
        updater = Updater(self.token, use_context=True)

        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self.start))

        updater.start_polling()
        updater.idle()


    def start(self, update, context):
        """
        Обработка кнопки "Старт" в чате с ботомd
        """
        chat = update.effective_chat
        context.bot.send_message(chat_id=chat.id, text="Привет, я крипто бот")

def b():
    """_sum875785mary_
    """