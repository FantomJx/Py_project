from telebot import types
import telebot
import face_detection
import requests

bot = telebot.TeleBot('5830243610:AAFOtgF7pX5bZUnufGacrvRJwmIcyQtsZ_U')
API = '3f90c731689673e0a4c127037eeb1a67'


@bot.message_handler(commands=['site'])
def site(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Go to site', url='https://openweathermap.org'))
    bot.reply_to(message, 'Visit site', reply_markup=markup)


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton('Find faces', callback_data='Find')
    btn1 = types.InlineKeyboardButton('Turn to binary', callback_data='Binary')
    markup.row(btn, btn1)
    bot.reply_to(message, 'Actions with photo', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'Find':
        bot.send_photo(callback.message.chat.id, face_detection.find_face(callback.message.id))
    elif callback.data == 'Binary':
        bot.send_photo(callback.message.chat.id, face_detection.find_face(callback.message.id))


@bot.message_handler(commands=['weather'], kwargs=)
def weather(message):
    bot.send_message(message.chat.id, 'Enter town ')

    @bot.message_handler(content_types=['text'])
    def get_weather(_message):
        city = _message.text.strip().lower()
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
        bot.reply_to(message, f'The weather now: {res.json()}')


@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, 'This bot will display the weather in the town which you choose')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'Id: {message.from_user.id}')


bot.polling(non_stop=True)
