import random
import re
import urllib.request as urllib2
import requests
import telebot
from telebot import types
bot = telebot.TeleBot('5904919278:AAHAkV48iuxxqEtqE6nxvnNNzW6AsaxBMIs')

def new_cat():
    x = random.randint(1, 1677)
    url = 'https://aws.random.cat/view/' + str(x)
    content = urllib2.urlopen(url).read()
    s = str(content)
    imgUrls = re.findall('img .*?src="(.*?)"', s)
    st = str(imgUrls[0])
    p = requests.get(imgUrls[0])
    if st.endswith('.gif'):
        out = open('image.gif', "wb")
        out.write(p.content)
        out.close()
        return 0
    else:
        out = open('img.png', "wb")
        out.write(p.content)
        out.close()
        return 1

def simple_keyboard(needid, cat_pic):
    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text='Да!', callback_data='Yes')
    but_2 = types.InlineKeyboardButton(text='Конечно!', callback_data='Sure')
    but_3 = types.InlineKeyboardButton(text='Давай!', callback_data='Definitely')
    key.add(but_1, but_2, but_3)
    bot.send_photo(needid, cat_pic, 'Хочешь еще котиков?', reply_markup=key)

@bot.message_handler(commands=['start'])
def inline_start(start_message):
    first_cat = open('img_1.png', 'rb')
    simple_keyboard(start_message.chat.id, first_cat)

@bot.callback_query_handler(func = lambda call: True)
def inline_query(call):
    if (new_cat() == 1):
        cat = open('img.png', 'rb')
    else:
        cat = open('image.gif', 'rb')
    if (call.data == 'Yes') or (call.data == 'Sure') or (call.data == 'Definitely'):
        simple_keyboard(call.message.chat.id, cat)
    else:
        bot.send_message(call.message.chat.id, 'Что-то пошло не так...')

@bot.message_handler(content_types=['text'])
def inline_text(message):
    first_cat = open('img_1.png', 'rb')
    love_cat = open('img_2.png', 'rb')
    if (new_cat() == 1):
        cat = open('img.png', 'rb')
    else:
        cat = open('image.gif', 'rb')
    if (message.text == 'Привет') or (message.text == 'Приветик'):
        simple_keyboard(message.chat.id, first_cat)
    elif (message.text == 'Да') or (message.text == 'Конечно') or (message.text == 'Хочу') or (message.text == 'Хочу ещё') or (message.text == 'Давай'):
        simple_keyboard(message.chat.id, cat)
    elif message.text == 'Люблю тебя':
        simple_keyboard(message.chat.id, love_cat)
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю...')
        key = types.InlineKeyboardMarkup()
        but = types.InlineKeyboardButton(text='Хочу картинку котика', callback_data='Yes')
        key.add(but)
        bot.send_message(message.chat.id, 'Нажми на кнопочку ниже', reply_markup=key)

bot.polling(none_stop=True, interval=0)
