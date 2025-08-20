import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
import time
from translate import get_translate_wooo, get_translate_google, get_translate
from aiogram.filters import Command
import random
from aiogram.fsm.state import State, StatesGroup
import db

def keyboard(original_word):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="wooordhunt", 
        callback_data=f"wooordhunt:{original_word}"
    )
    return builder.as_markup()

TOKEN = ''
BOT = Bot(token=TOKEN)
dp = Dispatcher()
sample = f'loading...'


class AddWord(StatesGroup):
    waiting_for_word = State()
    waiting_for_dell = State()

def keyboard_learn(word, translate):
    builder = InlineKeyboardBuilder()
    builder.button(
        text='translate',
        callback_data=f'{word},{translate}'
    )
    return builder.as_markup()

def keyboard_translate(word, google_translate):
    builder = InlineKeyboardBuilder()
    builder.button(
        text='wooordhunt',
        callback_data=f'wooordhunt:{word}'
    )
    builder.button(
        text='add',
        callback_data=f'add:{word},{google_translate}'
    )
    return builder.as_markup()

def keyboard_add(word, translate):
    builder = InlineKeyboardBuilder()
    builder.button(
        text='add',
        callback_data=f'add:{word},{translate}'
    )
    return builder.as_markup()

def next_word():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='next',
        callback_data='next'
    )
    return builder.as_markup()

@dp.message(Command("start"))
async def start(message):
    user = message.from_user.username
    words = db.get_words(user)
    if not words:
        await message.answer("Добро пожаловать")
        await message.answer("Ваш список слов пуст")
    else:
        word, translate = random.choice(words)[0].split(' - ')
        await message.answer(word, reply_markup=keyboard_learn(word, translate))

@dp.message(Command("add"))
async def add(message, state):
    await message.answer("Введите слово в формате: слово - перевод")
    await state.set_state(AddWord.waiting_for_word)

@dp.message(AddWord.waiting_for_word)
async def process_word(message, state):
    user = message.from_user.username
    input_text = message.text
    if ' - ' not in input_text:
        await message.answer("Неверный формат. Используйте: слово - перевод")
        return
    db.add_word(user, input_text)
    await message.answer("Слово добавлено")
    await state.clear()

@dp.message(Command("del"))
async def dell(message, state):
    await message.answer("Введите слово")
    await state.set_state(AddWord.waiting_for_dell)

@dp.message(AddWord.waiting_for_dell)
async def process_dell(message, state):
    user = message.from_user.username
    input_text = message.text
    db.del_word(user, input_text)
    await message.answer("ок - 👍")
    await state.clear()

@dp.message(F.text)
async def take_word(message):
    if '/' not in message.text:
        word = message.text
        print(f'{time.strftime("%H:%M:%S")}|[{message.from_user.first_name} {message.from_user.username}]: {message.text}')
        bot_message = await message.answer(sample)
        google_translate = await get_translate_google(word)
        bot_message = await bot_message.edit_text(google_translate, reply_markup=keyboard_add(word, google_translate))
        print(f'{time.strftime("%H:%M:%S")}|[бот]: {google_translate}')
        wooo_translate = await get_translate_wooo(word)
        if wooo_translate: await bot_message.edit_text(google_translate, reply_markup=keyboard_translate(word, google_translate))    

@dp.callback_query()
async def callback(query):
    message = query.message
    callback_data = query.data
    user = query.from_user.username
    words = db.get_words(user)
    if callback_data == 'next':
        if not words:
            await message.answer("Ваш список слов пуст")
        else:
            word, translate = random.choice(words)[0].split(' - ')
            await message.edit_text(word, reply_markup=keyboard_learn(word, translate))

    elif 'wooordhunt:' in callback_data:
        word = callback_data.split(':')[1]
        await message.edit_text(sample)
        wooo_translate = await get_translate_wooo(word)
        await message.edit_text(wooo_translate)
        print(f'{time.strftime("%H:%M:%S")}|[бот call]: {wooo_translate}')
    elif 'add:' in callback_data:
        word, translate = callback_data.split(':')[1].split(',')
        db.add_word(user, f'{word} - {translate}')
    else:
        await message.edit_text(f'{callback_data.split(',')[0]} - {callback_data.split(',')[1]}', reply_markup=next_word())


async def main():
    db.init()
    print("Bot started")
    await dp.start_polling(BOT)

if __name__ == "__main__":
    asyncio.run(main())