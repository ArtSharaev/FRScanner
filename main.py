import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import TOKEN
from fr24.get_data import get_flights


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s]'
                           u' %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG,
                    filename='logging.log',
                    filemode='w')
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Всем привет, это бот - сканер FR24\n"
                        "Чтобы начать работу, введи команду /help", reply=False)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Пока что тут не густо. Введите ICAO-код авиакомпании!")


@dp.message_handler()
async def echo_message(msg: types.Message):
    for flight in get_flights(msg.text):
        print(flight)
        photo = flight["photo"]
        caption = flight["info"]
        if photo:
            await bot.send_photo(msg.from_user.id, photo=photo, caption=caption)
        else:
            await bot.send_message(msg.from_user.id, caption)


if __name__ == '__main__':
    executor.start_polling(dp)