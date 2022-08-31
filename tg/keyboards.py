from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

empty_kb = ReplyKeyboardRemove()

skip_airport_choice_btn = KeyboardButton("skip")
skip_airport_choice_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                             one_time_keyboard=True).add(
    skip_airport_choice_btn)

get_flights_btn = KeyboardButton("/getflights")
get_flights_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True).add(
    get_flights_btn)
