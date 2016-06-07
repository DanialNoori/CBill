import urllib

__author__ = 'Danial'

import telebot
from telebot import types
import requests, io
from io import BytesIO
from PIL import Image
from urllib import request

myBot = telebot.TeleBot('227811575:AAHLWBh035jMtwlzcPib75y9RoV8xWydML8')

@myBot.message_handler(commands=['help', 'start'])
def begin(message):
    welcome_message = 'سلام، من سیبیلم! \n' \
                      'اسم هر فیلم یا سریالی که میخواید رو برام بفرستید تا اطلاعاتش رو بهتون بدم.'
    myBot.reply_to(message, welcome_message)


class Normalizer():
    def movie_name_editor(movie_name):
        return movie_name.replace(' ', '+')


@myBot.message_handler(func=lambda m: True)
def movie_search(message):
    try:
        movie_name = message.text
        normal_movie_name = Normalizer.movie_name_editor(movie_name)
        omdbpi_response = requests.get('http://www.omdbapi.com/?t=' + normal_movie_name + '&r=json')
        data = omdbpi_response.json()
        if data['Response'] == 'True':
            title = data['Title']
            director = data['Director']
            plot = data['Plot']
            genre = data['Genre']
            actors = data['Actors']
            poster_url = data['Poster']
            imdb_rating = data['imdbRating']
            year = data['Year']
            response = 'اسم فیلم/سریال:' + '\n' + title + ' '+'('+year + ')' + '\n' + 'کارگردان:' + '\n' + director + '\n'
            response += 'بازیگران:' + '\n' + actors + '\n'
            response += 'ژانر:' + '\n' + genre + '\n' + 'امتیاز کاربران:' + '\n' + imdb_rating + '/10'+'\n'+ 'خلاصه داستان:' +'\n' + plot
            response += '\n' + 'پوستر فیلم:' + '\n' + poster_url
            myBot.reply_to(message, response)
        else:
            excuse_us = 'متاسفانه این فیلم رو نمیشناسم!'
            myBot.reply_to(message, excuse_us)
    except Exception as e:
        myBot.reply_to(message, 'وات؟!')

myBot.polling()