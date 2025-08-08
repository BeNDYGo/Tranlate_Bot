import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
import time
from translate import get_translate

def keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="wooordhunt", callback_data="wooordhunt")
    keyboard = builder.as_markup()
    return keyboard

TOKEN = '7772137371:AAHr8CudNzCombH0CWf4D5DHacw1Eo3U43E'

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(~F.command)
async def take_word(message):
    if '/' in message.text: return 
    word = message.text
    wooo_translate, google_translate = await get_translate(word)
    result = google_translate
    if wooo_translate: await message.answer(result, reply_markup=keyboard())
    else: await message.answer(result)

    print(f'{time.strftime("%H:%M:%S")}|[{message.from_user.first_name} {message.from_user.username}]: {message.text}')
    print(f'{time.strftime("%H:%M:%S")}|[бот]: {result}')

@dp.callback_query(F.data.startswith("wooordhunt"))
async def callback_handler(callback):
    word = callback.message.text
    wooo_translate, google_translate = await get_translate(word)
    result = wooo_translate
    await callback.message.edit_text(result)

print("Начало нового сеанса")
async def main(): await dp.start_polling(bot)
asyncio.run(main())