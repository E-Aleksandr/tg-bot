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
<b>УЧАСТНИКИ ТУРНИРА <a href="https://t.me/c/1657644603/411360/603092">"В ДВА СТВОЛА"</a> И ИХ СТАТИСТИКА</b>

<blockquote>КБ – количество боëв
ПП – процент побед
СУ – средний урон</blockquote>
"""

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝ИНФА И ПРАВИЛА", web_app=WebAppInfo(url="https://t.me/c/1657644603/411360/603092"))],
        [InlineKeyboardButton(text="🎬ВИДЕО ЖЕРЕБЬЁВКИ", web_app=WebAppInfo(url="https://t.me/c/1657644603/411360/610175")),
         InlineKeyboardButton(text="⚙️ТУРНИРНАЯ СЕТКА", web_app=WebAppInfo(url="https://t.me/c/1657644603/411360/615492"))],
         [InlineKeyboardButton(text="✅ПРОГНОЗЫ", web_app=WebAppInfo(url="https://site2-production-29a1.up.railway.app"))]
    ])
    await message.answer(msg, reply_markup=keyboard)

async def main():
    print("✅ Бот запущен! v1.1")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
