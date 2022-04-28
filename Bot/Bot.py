"""This module contains an object that represents a Telegram Bot."""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from .CMC_interact import CMC_API as cmc


class Bot:
    """_summary_
    """
    
    token = '5175481555:AAEp0UQJs1nWZxFQonsFvHDktGfHPZewwq0'
    
    def __init__(self):
        updater = Updater(self.token, use_context=True)

        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("help", self.help))
        dispatcher.add_handler(CommandHandler("id", self.id))

        updater.start_polling()
        updater.idle()


    def start(self, update, context):
        """
        Обработка кнопки "Старт" в чате с ботом
        """
        chat = update.effective_chat
        context.bot.send_message(chat_id=chat.id, text="Привет, я крипто бот")


    def help(self, update, context):
        """
        Обработка команды "Help"
        """
        chat = update.effective_chat
        context.bot.send_message(chat_id=chat.id, text="Список команд:\n/id")


    def id(self, update, context):
        """
        Обработка команды получения id криптовалюты
        """
        chat = update.effective_chat
        symb = ' '.join(context.args)
        context.bot.send_message(chat_id=chat.id, text=cmc.get_CMC_id(cmc(), symb))


def b():
    """_summary_
    """

a = Bot()