from aiogram import types
from tg.messages import MESSAGES
from tg.utils import States
from tg.keyboards import skip_airport_choice_kb, get_flights_kb
from fr24.get_data import get_flights, fr_api

from main import dp, bot


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(MESSAGES["start"], reply=False,
                        reply_markup=get_flights_kb)


@dp.message_handler(commands=['getflights'])
async def process_get_flights_command(msg: types.Message):
    await bot.send_message(msg.from_user.id, MESSAGES["ask_airline"])
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.all()[1])


@dp.message_handler(state=States.SET_AIRLINE)
async def set_airline(msg: types.Message):
    await bot.send_message(msg.from_user.id, MESSAGES["ask_airport"],
                           reply_markup=skip_airport_choice_kb)
    state = dp.current_state(user=msg.from_user.id)
    await state.update_data(airline=msg.text.upper())
    await state.set_state(States.all()[0])


@dp.message_handler(state=States.GET_RESULT)
async def get_result(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)
    state_data = await state.get_data()
    if msg.text == "skip":
        airport = None
    else:
        airport = msg.text
    airline_flights = fr_api.get_flights(airline=state_data["airline"].upper())
    if airline_flights:
        await bot.send_message(msg.from_user.id, f"{len(airline_flights)} "
                                                 f"aircraft of the specified "
                                                 f"airline were found.\n"
                                                 f"Filtering...")

        for flight in get_flights(state_data["airline"], airport):
            print(flight)
            photo = flight["photo"]
            caption = flight["info"]
            if photo:
                await bot.send_photo(msg.from_user.id, photo=photo,
                                     caption=caption)
            else:
                await bot.send_message(msg.from_user.id, caption)

        await bot.send_message(msg.from_user.id, MESSAGES["done"],
                               reply_markup=get_flights_kb)
    else:
        await bot.send_message(msg.from_user.id, "",
                               reply_markup=get_flights_kb)
    await state.finish()
