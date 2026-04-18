# bot.py
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command

BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

msg = """
В ДВА СТВОЛА

Турнир в новом формате с улучшенным балансом. Теперь одержать победу сможет каждый, не зависимо от статы и скилла!

Участники делятся на пары, затем составляется турнирная сетка. Происходит PvP сражение между командами, победитель переходит в следующий раунд. Лучший дуэт побеждает в турнире.
"""

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подробности", web_app=WebAppInfo(url="https://telegra.ph/V-DVA-STVOLA-04-18-3"))],
        [InlineKeyboardButton(text="Прогнозы", web_app=WebAppInfo(url="https://site2-production-29a1.up.railway.app"))]
    ])
    await message.answer(msg, reply_markup=keyboard)

async def main():
    print("✅ Бот запущен! v1.1")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
