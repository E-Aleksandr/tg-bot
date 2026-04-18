# bot.py
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from aiogram.types import FSInputFile
from urllib.parse import urlencode

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_IDS = [1723402881]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

msg = """
УЧАСТНИКИ ТУРНИРА <a href="https://t.me/c/1657644603/411360/603092"><b>"В ДВА СТВОЛА"</b></a>

<blockquote><b>Основные показатели:</b>
• <b>КБ</b> <i>— количество боёв</i>
• <b>ПП</b> <i>— процент побед</i>  
• <b>СУ</b> <i>— средний урон</i></blockquote>
"""

@dp.message(Command("post"))
async def post_cmd(message: types.Message):
    user = message.from_user

    if message.from_user.id not in ADMIN_IDS:
        await message.reply("Иди нахуй")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 ИНФА И ПРАВИЛА", url="https://t.me/c/1657644603/411360/603092")],
        [InlineKeyboardButton(text="🎬 ЖЕРЕБЬЁВКА", url="https://t.me/c/1657644603/411360/610175"),
         InlineKeyboardButton(text="⚙️ ТУР СЕТКА", url="https://t.me/c/1657644603/411360/615492")],
        [InlineKeyboardButton(text="✅ ПРОГНОЗЫ", url="https://site2-production-29a1.up.railway.app")]
    ])
    await message.answer_photo(photo=FSInputFile("setka.jpg"), parse_mode="HTML", caption=msg, reply_markup=keyboard)

async def main():
    print("✅ Бот запущен! v1.2")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
