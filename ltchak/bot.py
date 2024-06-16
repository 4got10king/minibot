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


@dp.message(lambda message: message.text.isdigit())
async def get_company_info(message: types.Message):
    api_key = "amp5SkbhXJOrm8g8"
    inn = message.text

    url = f"https://api.checko.ru/v2/company?key={api_key}&inn={inn}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        chat_id = message.chat.id
        document = FSInputFile("data.json")
        await bot.send_document(document=document, chat_id=chat_id)

    else:
        await message.answer("Ошибка при выполнении запроса")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
