import datetime
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from keepalive import keep_alive
import keys  # your API keys

bot = Bot(token=keys.tg_key)
dp = Dispatcher(bot)
weather_key = keys.weather_key

keep_alive()

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("HI! Send me a city name and I will send weather info about this city 🌤️")

@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        city_name = message.text
        url = f"http://api.weatherapi.com/v1/current.json?key={weather_key}&q={city_name}&aqi=no"
        r = requests.get(url)
        data = r.json()

        if "error" in data:
            await message.reply("☠ Check city name or API error ☠")
            print("WeatherAPI error:", data["error"]["message"])
            return

        location = data["location"]
        current = data["current"]

        city = location["name"]
        country = location["country"]
        temp_c = current["temp_c"]
        condition = current["condition"]["text"]
        humidity = current["humidity"]
        wind_kph = current["wind_kph"]
        last_updated = current["last_updated"]

        await message.reply(
            f"🌍 Weather in {city}, {country}\n"
            f"🌡️ Temperature: {temp_c}°C\n"
            f"⛅ Condition: {condition}\n"
            f"💧 Humidity: {humidity}%\n"
            f"🌬️ Wind: {wind_kph} km/h\n"
            f"🕒 Last Updated: {last_updated}\n"
            f"✨ Have a great day!"
        )

    except Exception as e:
        await message.reply("⚠️ An error occurred. Try again later.")
        print("Exception:", e)

executor.start_polling(dp)
