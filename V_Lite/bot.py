import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.command import Command
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
import time
from V_Full.translate import get_translate_wooo, get_translate_google, get_translate

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

@dp.message(Command("start"))
async def handle_start(message: types.Message):
    await message.answer("Hello! I'm a bot that can translate words.")

@dp.message(Command("tr"))
async def handle_tr(message: types.Message):
    word = message.text[4:]
    print(f'{time.strftime("%H:%M:%S")}|[{message.from_user.first_name} {message.from_user.username}]: {word}')
    bot_message = await message.reply(sample)
    google_translate = await get_translate_google(word)
    bot_message = await bot_message.edit_text(google_translate)
    print(f'{time.strftime("%H:%M:%S")}|[бот]: {google_translate}')
    wooo_translate = await get_translate_wooo(word)
    if wooo_translate:
        await bot_message.edit_text(google_translate, reply_markup=keyboard(word))

@dp.message(F.text)
async def take_word(message):
    word = message.text
    if word[0] == '/': return
    print(f'{time.strftime("%H:%M:%S")}|[{message.from_user.first_name} {message.from_user.username}]: {message.text}')
    bot_message = await message.answer(sample)
    google_translate = await get_translate_google(word)
    await bot_message.edit_text(google_translate)
    print(f'{time.strftime("%H:%M:%S")}|[бот]: {google_translate}')
    wooo_translate = await get_translate_wooo(word)
    if wooo_translate: await bot_message.edit_text(google_translate, reply_markup=keyboard(word))

@dp.callback_query(F.data.startswith("wooordhunt:"))
async def callback_handler(callback):
    word = callback.data.split(":", 1)[1]
    await callback.message.edit_text(sample)
    wooo_translate = await get_translate_wooo(word)
    await callback.message.edit_text(wooo_translate)
    print(f'{time.strftime("%H:%M:%S")}|[бот call]: {wooo_translate}')

@dp.inline_query()
async def inline_echo(inline_query: types.InlineQuery):
    text = inline_query.query
    translate = await get_translate_google(text)
    result = InlineQueryResultArticle(
        id="1",
        title="Top_Traanslate_bot",
        description=f"Translate",
        input_message_content=InputTextMessageContent(message_text=f"{translate}")
    )
    await inline_query.answer([result], cache_time=1, is_personal=True)

print("Начало нового сеанса")
async def main(): await dp.start_polling(bot)
asyncio.run(main())
