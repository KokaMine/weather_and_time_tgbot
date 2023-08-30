from datetime import datetime

import pytz
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command

from data import config
from loader import dp
from states.all_info import AllInfo
from mtranslate import translate

def time_info(city):
    URL = f"http://api.weatherapi.com/v1/current.json?key={config.weather_api_key}&q={city}&aqi=no"
    response = requests.get(URL).json()
    city_tz = pytz.timezone(response["location"]["tz_id"])

    time = (f'Time in the {city} {datetime.now(tz=city_tz).strftime("%H:%M - %m.%d.%Y")}' )

    return time

@dp.message_handler(Command("time"))
async def call_time(message: types.Message):
    await message.answer('Напишите город, в котором хотите узнать время:')

    await AllInfo.q_2.set()


@dp.message_handler(state=AllInfo.q_2)
async def get_time(message: types.Message, state: FSMContext):
    try:
        await message.answer(translate(time_info(translate(message.text, "en", "ru")),"ru","en"))

        await state.reset_state()

    except KeyError:
        await message.answer("Это не город. Попробуйте ещё раз.")


