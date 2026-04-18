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
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("Иди нахуй")
        return
    
    user = message.from_user
    username = user.username or f"user_{user.id}"
    params = urlencode({"username": username, "user_id": user.id})

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 ИНФА И ПРАВИЛА", url="https://t.me/c/1657644603/411360/603092")],
        [InlineKeyboardButton(text="🎬 ЖЕРЕБЬЁВКА", url="https://t.me/c/1657644603/411360/610175"),
         InlineKeyboardButton(text="⚙️ ТУР СЕТКА", url="https://t.me/c/1657644603/411360/615492")],
        [InlineKeyboardButton(text="✅ ПРОГНОЗЫ", url=f"https://site2-production-29a1.up.railway.app?{params}")]
    ])
    await message.answer_photo(photo=FSInputFile("setka.jpg"), parse_mode="HTML", caption=msg, reply_markup=keyboard)

async def main():
    print("✅ Бот запущен! v1.1")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
