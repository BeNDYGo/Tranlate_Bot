import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
import time
from translate import get_translate_wooo, get_translate_google, get_translate

def keyboard(original_word):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="wooordhunt", 
        callback_data=f"wooordhunt:{original_word}"
    )
    return builder.as_markup()

TOKEN = ''

bot = Bot(token=TOKEN)
dp = Dispatcher()

sample = f'loading...'

@dp.message(~F.command & F.text)
async def take_word(message):
    word = message.text
    if '/' in word: return
    print(f'{time.strftime("%H:%M:%S")}|[{message.from_user.first_name} {message.from_user.username}]: {message.text}')
    bot_message = await message.answer(sample)
    google_translate = await get_translate_google(word)
    bot_message = await bot_message.edit_text(google_translate)
    print(f'{time.strftime("%H:%M:%S")}|[бот]: {google_translate}')
    wooo_translate = get_translate_wooo(word)
    if wooo_translate: await bot_message.edit_text(google_translate, reply_markup=keyboard(word))

@dp.callback_query(F.data.startswith("wooordhunt:"))
async def callback_handler(callback):
    word = callback.data.split(":", 1)[1]
    await callback.message.edit_text(sample)
    wooo_translate = await get_translate_wooo(word)
    await callback.message.edit_text(wooo_translate)
    print(f'{time.strftime("%H:%M:%S")}|[бот call]: {wooo_translate}')

print("Начало нового сеанса")
async def main(): await dp.start_polling(bot)
asyncio.run(main())
