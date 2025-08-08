import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
import time
from translate import get_translate

def keyboard(original_word):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="wooordhunt", 
        callback_data=f"wooordhunt:{original_word}"  # Добавляем слово в callback
    )
    return builder.as_markup()

TOKEN = '8106791048:AAE0GUGxMnzEE_sOH87rCdjqpW_rp7Uyz2o'

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(~F.command)
async def take_word(message):
    if '/' in message.text: return 
    word = message.text
    wooo_translate, google_translate = await get_translate(word)
    result = google_translate
    if wooo_translate: await message.answer(result, reply_markup=keyboard(word))
    else: await message.answer(result)

    print(f'{time.strftime("%H:%M:%S")}|[{message.from_user.first_name} {message.from_user.username}]: {message.text}')
    print(f'{time.strftime("%H:%M:%S")}|[бот]: {result}')

@dp.callback_query(F.data.startswith("wooordhunt:"))
async def callback_handler(callback):
    word = callback.data.split(":", 1)[1]
    wooo_translate, google_translate = await get_translate(word)
    result = wooo_translate
    await callback.message.edit_text(result)

print("Начало нового сеанса")
async def main(): await dp.start_polling(bot)
asyncio.run(main())
