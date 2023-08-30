from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, state

from loader import dp
from states.all_info import AllInfo
from mtranslate import translate
import requests
from data import config

def weather_(city):
    URL = f"http://api.weatherapi.com/v1/current.json?key={config.weather_api_key}&q={city}&aqi=no"
    response = requests.get(URL).json()

    weather_city = (f'The weather in {city} is {response["current"]["condition"]["text"]}.\n'
                  f'The temperature is {response["current"]["temp_c"]}°C\n'
                  f'Wind direction: {response["current"]["wind_dir"]}\n'
                  f'Wind speed: {response["current"]["wind_kph"]} км/ч\n'
                  f'Pressure: {round(response["current"]["pressure_mb"]*0.7500637554192, 1)} мм.рт.ст.\n'
                  f'Humidity: {response["current"]["humidity"]}%')

    return weather_city

@dp.message_handler(Command("weather"))
async def choose_city(message: types.Message):
    await message.answer("Напишите город, в котором хотите узнать погоду:")

    await AllInfo.q_1.set()

@dp.message_handler(state=AllInfo.q_1)
async def get_weather(message: types.Message, state: FSMContext):
    try:
        await message.answer(translate(weather_(translate(message.text, "en", "ru")), "ru", "en"))

        await state.reset_state()

    except KeyError:
        await message.answer("Это не город. Попробуйте ещё раз.")