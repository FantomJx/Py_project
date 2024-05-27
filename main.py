from telebot import types
# import openai
import telebot
import face_detection
import requests
import json
import os

bot = telebot.TeleBot('5830243610:AAFOtgF7pX5bZUnufGacrvRJwmIcyQtsZ_U')
API = '3f90c731689673e0a4c127037eeb1a67'


@bot.message_handler(commands=['site'])
def site(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Go to site', url='https://openweathermap.org'))
    bot.reply_to(message, 'Visit site', reply_markup=markup)


@bot.message_handler(commands=['photo'])
def chat_photo(message):
    bot.send_message(message.chat.id, 'Send photo ')

    @bot.message_handler(content_types=['photo'])
    def get_photo(_message):
        raw = _message.photo[1].file_id
        path = "photos/" + raw + ".jpg"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(path, 'wb') as new_file:
            new_file.write(downloaded_file)
            os.rename(f'{path}', 'photos/photo.jpg')
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('Find faces', callback_data='Find')
        btn1 = types.InlineKeyboardButton('Turn to binary', callback_data='Binary')
        markup.row(btn, btn1)
        bot.reply_to(message, 'Actions with photo', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    path = 'photos/photo.jpg'
    file = open(f'{path}', 'rb')
    if callback.data == 'Find':
        face_detection.find_face(path)
        bot.send_photo(callback.message.chat.id, file)
    elif callback.data == 'Binary':
        face_detection.to_binary(path)
        bot.send_photo(callback.message.chat.id, file)
    for file in os.listdir('photos/'):
        if file.endswith('.png'):
            os.remove(file)


@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id, 'Are you going to touch the grass?\nEnter town ')

    @bot.message_handler(content_types=['text'])
    def get_weather(_message):
        city = _message.text.strip().lower()
        isCity = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={API}')
        data = json.loads(isCity.text)
        if range(len(data)):
            lat = data[0]['lat']
            lon = data[0]['lon']
            res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API}'
                               f'&units=metric')
            data = json.loads(res.text)
            temp = data['main']['temp']
            _weather = data['weather'][0]['main']
            bot.send_message(_message.chat.id, f'The weather in {_message.text} is {_weather}\n'
                                               f'The temperature is {round(temp, 1)}')
        else:
            bot.reply_to(_message, 'There is not that town')


# @bot.message_handler(commands=['gpt'])
# def gpt(message):
#     bot.send_message(message.chat.id, 'Enter your question ')
#
#     @bot.message_handler(content_types=['text'])
#     def question(_message):
#         completion = openai.Completion.create(engine="gpt-3.5-turbo", prompt=f"{_message}")
#         bot.reply_to(_message.chat.id, f"{completion.choices[0].text}")


@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, 'This bot will display the weather in the town which you choose')


bot.polling(non_stop=True)
