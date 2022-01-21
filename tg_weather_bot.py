import requests
import datetime
from weather_bot_token import weather_bot_token
from openweathermap_api_token import api_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=weather_bot_token)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(
        "Привет дружок! С моей помощью ты легко сможешь узнать погоду в любом городе! Просто введи его название и наслаждайся магией!")


@dispatcher.message_handler()
async def get_weather(message: types.Message):
    try:
        req = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={api_token}&units=metric")
        data = req.json()
        city = data["name"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        feels_like_temperature = data["main"]["feels_like"]
        max_temperature = data["main"]["temp_max"]
        min_temperature = data["main"]["temp_min"]
        await message.reply(f"Текущая дата: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                            f"Погода в городе {city}:\nТемпература: {temperature} ℃\n"
                            f"Максимальная температура: {max_temperature} ℃\nМинимальная температура: {min_temperature} ℃\n"
                            f"Ощущается как: {feels_like_temperature} ℃\nСкорость ветра: {wind_speed} м/с\n"
                            f"Влажность: {humidity} %\nДавление: {pressure} мм.рт.ст."
                            )
    except:
        await message.reply("Что-то не так...\nПроверьте название города")


if __name__ == '__main__':
    executor.start_polling(dispatcher)
