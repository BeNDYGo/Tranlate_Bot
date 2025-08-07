import telebot
from translate import *
import time

TOKEN = "8106791048:AAE0GUGxMnzEE_sOH87rCdjqpW_rp7Uyz2o"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcom(message):
    bot.send_message(message.chat.id, 'Пришли слово для перевода')

@bot.message_handler(func=lambda _: True)
def take_word(message):
    print(f'{time.strftime("%H:%M:%S")}|[{message.from_user.first_name} {message.from_user.username}]: {message.text}')
    result = get_translate(message.text)
    print(f'{time.strftime("%H:%M:%S")}|[бот]: {result}')
    if result: bot.send_message(message.chat.id, str(result))
    else: bot.send_message(message.chat.id, str('ошибка'))


print("Начало нового сеанса")
# Запуск бота
bot.polling(none_stop=True)



















'''import telebot
from translate import *
from bd import *

TOKEN = "8106791048:AAE0GUGxMnzEE_sOH87rCdjqpW_rp7Uyz2o"
bot = telebot.TeleBot(TOKEN)
init_db()

@bot.message_handler(commands=['start'])
def welcom(message):
    set_user_flag(message.chat.id, True)
    bot.send_message(message.chat.id, 'Пришли слово для перевода')

@bot.message_handler(func=lambda _: True)
def take_word(message):
    print(message.from_user.first_name, message.from_user.username ,message.text)

    if get_user_flag(message.chat.id):
        set_user_flag(message.chat.id, False)
        result = get_translate(message.text)
        print(f'бот ответил {result}')
        if result: bot.send_message(message.chat.id, str(result))
        else: bot.send_message(message.chat.id, str('ошибка'))


print("Начало нового сеанса")
# Запуск бота
bot.polling(none_stop=True)
'''