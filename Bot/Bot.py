"""This module contains an object that represents a Telegram Bot."""

#from telegram.ext import Updater, CommandHandler
from email import message
from CMC_interact import CMC_API as cmc
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import logging


"""_summary_
"""

tok = '5175481555:AAEp0UQJs1nWZxFQonsFvHDktGfHPZewwq0'
bot = Bot(token = '5175481555:AAEp0UQJs1nWZxFQonsFvHDktGfHPZewwq0')
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    """
    Обработка кнопки "start" в чате с ботом
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = ["restart"]
    keyboard.add(*button)
    await message.answer("Привет, я крипто бот\n" + "Введи команду" + " /help" + ", чтобы получить информацию о доступных командах!", reply_markup=keyboard)


@dp.message_handler(Text(equals="restart"))
async def restart(message: types.Message):
    await message.answer("Привет, я крипто бот\n" + "Введи команду" + " /help" + ", чтобы получить информацию о доступных командах!", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands="help")
async def help(message: types.Message):
    """
    Обработка команды "help"
    """

    buttons = [
        types.InlineKeyboardButton(text="/btc"),
        types.InlineKeyboardButton(text="/support"),
        types.InlineKeyboardButton(text="/help")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    await message.answer("Список доступных команд:\n" + 
                        "/btc" + " - полная статистика по BTC\n" +
                        "/stat" + " + название токена - полная статистика по введенному токену\n" +
                        "/support" + " - техническая поддержка бота\n" +
                        "/help" + " - список доступных команд", reply_markup=keyboard)


@dp.message_handler(commands="support")
async def support(message: types.Message):
    """
    Обработка команды "support"
    """
    await message.answer("Поддержка: " + "\n@Borntowarn" + "\n@danyaalok")


@dp.message_handler(commands="btc")
async def btc(message: types.Message):
    """
    Обработка команды получения данных по BTC
    """
    prices = cmc.get_price_change(cmc(), 'btc', '1h, 24h')

    link = prices['BTC']['link']
    USD = prices['BTC']['price']['USD']['price']
    h_1 = prices['BTC']['price']['USD']['changes']['1h']
    h_24 = prices['BTC']['price']['USD']['changes']['24h']
    volumes = cmc.get_volume(cmc(), 'btc')
    volume = volumes['BTC']['volume']
    changes = volumes['BTC']['changes']

    await message.answer("Bitcoin | BTC" + '\n\n' + "Link: " + str(link) + "\n\nUSD: $" + str(USD) + 
            "\n\nPrice change:" + "\n1h: " + str(h_1) + "%" + "\n24h: " + str(h_24) + "%" + "\nMarket Cap: $" + str(volume) + "\n24h Volume: $" + str(changes))


@dp.message_handler(commands="stat")
async def stat(message: types.Message):
    """
    Обработка команды получения данных по введенному токену
    """
    try:
        symb = (message.get_args()).upper()
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

        await message.answer(full_name + '\n\n' + "Link: " + str(link) + "\n\nUSD: $" + str(USD) + 
                "\n\nPrice change:" + "\n1h: " + str(h_1) + "%" + "\n24h: " + str(h_24) + "%" + "\nMarket Cap: $" + str(volume) + "\n24h Volume: $" + str(changes))
    except:
        await message.answer("Я не понимаю Ваш запрос, попробуйте снова!")

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
    
if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)