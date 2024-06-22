import json

import requests
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import asyncio
from aiogram.types.input_file import FSInputFile

API_TOKEN = "7426163846:AAGdiknip1CFtUQvv8-LTbqyLRLGYw5B2-E"


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Пожалуйста, отправьте мне ИНН для получения данных о компании."
    )


async def get_data_from_multiple_sources(api_key, inn):
    data = {}

    endpoints = ["company", "legal-cases", "enforcements", "finances"]

    for endpoint in endpoints:
        url = f"https://api.checko.ru/v2/{endpoint}?key={api_key}&inn={inn}"
        response = requests.get(url)

        if response.status_code == 200:
            endpoint_data = response.json()
            data[endpoint] = endpoint_data

    with open("data.json", "a", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return data


@dp.message(lambda message: message.text.isdigit())
async def get_all_data(message: types.Message):
    api_key = "amp5SkbhXJOrm8g8"
    inn = message.text

    all_data = await get_data_from_multiple_sources(api_key, inn)

    chat_id = message.chat.id
    document = FSInputFile("data.json")
    await bot.send_document(document=document, chat_id=chat_id)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
