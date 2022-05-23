"""This module contains an object that represents a Telegram Bot."""

from telegram.ext import Updater, CommandHandler
from CMC_interact import CMC_API as cmc


class Bot:
    """_summary_
    """
    
    token = '5175481555:AAEp0UQJs1nWZxFQonsFvHDktGfHPZewwq0'
    
    def __init__(self):
        updater = Updater(self.token, use_context=True)

        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("help", self.help))
        dispatcher.add_handler(CommandHandler("btc", self.btc))
        dispatcher.add_handler(CommandHandler("stat", self.stat))
        dispatcher.add_handler(CommandHandler("support", self.support))

        updater.start_polling()
        updater.idle()


    def start(self, update, context):
        """
        Обработка кнопки "start" в чате с ботом
        """
        chat = update.effective_chat
        context.bot.send_message(chat_id=chat.id, text="Привет, я крипто бот\n" + "Введи команду" + " /help" + ", чтобы получить информацию о доступных командах!")


    def help(self, update, context):
        """
        Обработка команды "help"
        """
        chat = update.effective_chat
        context.bot.send_message(chat_id=chat.id, text="Список доступных команд:\n" + 
                                                        "/btc" + " - полная статистика по BTC\n" +
                                                        "/stat" + " + название токена - полная статистика по введенному токену\n" +
                                                        "/support" + " - техническая поддержка бота\n" +
                                                        "/help" + " - список доступных команд")

    
    def support(self, update, context):
        """
        Обработка команды "support"
        """
        chat = update.effective_chat
        context.bot.send_message(chat_id=chat.id, text="Поддержка: " + "\n@Borntowarn" + "\n@danyaalok")


    def btc(self, update, context):
        """
        Обработка команды получения данных по BTC
        """
        chat = update.effective_chat
        prices = cmc.get_price_change(cmc(), 'btc', '1h, 24h')

        link = prices['BTC']['link']
        USD = prices['BTC']['price']['USD']['price']
        h_1 = prices['BTC']['price']['USD']['changes']['1h']
        h_24 = prices['BTC']['price']['USD']['changes']['24h']
        volumes = cmc.get_volume(cmc(), 'btc')
        volume = volumes['BTC']['volume']
        changes = volumes['BTC']['changes']

        context.bot.send_message(chat_id=chat.id, text="Bitcoin | BTC" + '\n\n' + "Link: " + str(link) + "\n\nUSD: $" + str(USD) + 
        "\n\nPrice change:" + "\n1h: " + str(h_1) + "%" + "\n24h: " + str(h_24) + "%" + "\nMarket Cap: $" + str(volume) + "\n24h Volume: $" + str(changes))


    def stat(self, update, context):
        """
        Обработка команды получения данных по введенному токену
        """
        chat = update.effective_chat
        try:
            symb = (' '.join(context.args)).upper()
            prices = cmc.get_price_change(cmc(), symb, '1h, 24h')

            link = prices[symb]['link']
            USD = prices[symb]['price']['USD']['price']
            h_1 = prices[symb]['price']['USD']['changes']['1h']
            h_24 = prices[symb]['price']['USD']['changes']['24h']
            volumes = cmc.get_volume(cmc(), symb)
            volume = volumes[symb]['volume']
            changes = volumes[symb]['changes']
            name = volumes[symb]['name']
            full_name = name + " | " + symb

            context.bot.send_message(chat_id=chat.id, text= full_name + '\n\n' + "Link: " + str(link) + "\n\nUSD: $" + str(USD) + 
            "\n\nPrice change:" + "\n1h: " + str(h_1) + "%" + "\n24h: " + str(h_24) + "%" + "\nMarket Cap: $" + str(volume) + "\n24h Volume: $" + str(changes))
        except:
            context.bot.send_message(chat_id=chat.id, text="Я не понимаю Ваш запрос, попробуйте снова!")


a = Bot()