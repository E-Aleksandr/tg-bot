# bot.py
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command

WEBAPP_URL = os.environ.get("URL1")
WEBAPP_URL2 = os.environ.get("URL2")

bot = Bot(os.environ.get("BOT_TOKEN"))
dp = Dispatcher()

msg = """
В ДВА СТВОЛА

Турнир в новом формате с улучшенным балансом. Теперь одержать победу сможет каждый, не зависимо от статы и скилла!

Участники делятся на пары, затем составляется турнирная сетка. Происходит PvP сражение между командами, победитель переходит в следующий раунд. Лучший дуэт побеждает в турнире.
"""
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Бот готов!")

@dp.message(Command("post"))
async def start_cmd(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подробности", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    keyboard2 = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Прогнозы", web_app=WebAppInfo(url=WEBAPP_URL2))]
    ])
    await message.answer(msg, reply_markup=keyboard, reply_markup=keyboard2)

async def main():
    print("✅ Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
