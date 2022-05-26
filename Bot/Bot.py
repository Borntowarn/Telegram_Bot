"""This module contains an object that represents a Telegram Bot."""

from CMC_interact import CMC_API
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import logging


"""_summary_
"""

bot = Bot(token = '5175481555:AAEp0UQJs1nWZxFQonsFvHDktGfHPZewwq0')
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
cmc = CMC_API()


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
    await message.answer("Привет, я крипто бот\n" + "Введи команду" + " /help" + ", чтобы получить информацию о доступных командах!")


@dp.message_handler(commands="help")
async def help(message: types.Message):
    """
    Обработка команды "help"
    """

    buttons = [
        types.InlineKeyboardButton(text="/btc", callback_data="btc"),
        types.InlineKeyboardButton(text="/support", callback_data="support"),
        types.InlineKeyboardButton(text="/help", callback_data="help")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    await message.answer("Список доступных команд:\n" + 
                        "/btc" + " - полная статистика по BTC\n" +
                        "/stat" + " + название токена - полная статистика по введенному токену\n" +
                        "/support" + " - техническая поддержка бота\n" +
                        "/help" + " - список доступных команд", reply_markup=keyboard)


@dp.callback_query_handler(text="help")
async def send_help(call: types.CallbackQuery):
    """
    Обработка кнопки "help"
    """
    buttons = [
        types.InlineKeyboardButton(text="/btc", callback_data="btc"),
        types.InlineKeyboardButton(text="/support", callback_data="support"),
        types.InlineKeyboardButton(text="/help", callback_data="help")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    await call.message.answer("Список доступных команд:\n" + 
                        "/btc" + " - полная статистика по BTC\n" +
                        "/stat" + " + название токена - полная статистика по введенному токену\n" +
                        "/support" + " - техническая поддержка бота\n" +
                        "/help" + " - список доступных команд", reply_markup=keyboard)


@dp.callback_query_handler(text="support")
async def send_support(call: types.CallbackQuery):
    """
    Обработка кнопки "support"
    """
    await call.message.answer(support())


@dp.message_handler(commands="support")
async def support(message: types.Message):
    """
    Обработка команды "support"
    """
    await message.answer(support())


def support(): return("Поддержка: " + "\n@Borntowarn" + "\n@danyaalok")


@dp.message_handler(commands="btc")
async def btc(message: types.Message):
    """
    Обработка команды получения данных по BTC
    """
    await message.answer(btc())


@dp.callback_query_handler(text="btc")
async def send_btc(call: types.CallbackQuery):
    """
    Обработка кнопки "btc"
    """
    await call.message.answer(btc())


def btc():
    prices = cmc.get_price_change('btc', '1h, 24h')

    link = prices['BTC']['link']
    USD = prices['BTC']['price']['USD']['price']
    h_1 = prices['BTC']['price']['USD']['changes']['1h']
    h_24 = prices['BTC']['price']['USD']['changes']['24h']
    volumes = cmc.get_volume('btc')
    volume = volumes['BTC']['volume']
    changes = volumes['BTC']['changes']

    return("Bitcoin | BTC" + '\n\n' + "Link: " + str(link) + "\n\nUSD: $" + str(USD) + "\n\nPrice change:" + "\n1h: " + str(h_1) + "%" + "\n24h: " + str(h_24) + "%" + "\nMarket Cap: $" + str(volume) + "\n24h Volume: $" + str(changes))


@dp.message_handler(commands="stat")
async def stat(message: types.Message):
    """
    Обработка команды получения данных по введенному токену
    """
    try:
        symb = (message.get_args()).upper()
        await message.answer(stat(symb))
    except:
        await message.answer("Я не понимаю Ваш запрос, попробуйте снова!")


def stat(symb):
    prices = cmc.get_price_change(symb, '1h, 24h')

    link = prices[symb]['link']
    USD = prices[symb]['price']['USD']['price']
    h_1 = prices[symb]['price']['USD']['changes']['1h']
    h_24 = prices[symb]['price']['USD']['changes']['24h']
    volumes = cmc.get_volume(symb)
    volume = volumes[symb]['volume']
    changes = volumes[symb]['changes']
    name = volumes[symb]['name']
    full_name = name + " | " + symb
    return(full_name + '\n\n' + "Link: " + str(link) + "\n\nUSD: $" + str(USD) + "\n\nPrice change:" + "\n1h: " + str(h_1) + "%" + "\n24h: " + str(h_24) + "%" + "\nMarket Cap: $" + str(volume) + "\n24h Volume: $" + str(changes))


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)