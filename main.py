import telebot
import requests
from bs4 import BeautifulSoup
import random


token = '5521967872:AAEpu7Mm33L7yphxR4DtIxtvVB4vDE46BE4'
bot = telebot.TeleBot(token)

stickers = ['CAACAgIAAxkBAAEFB35ip3HOcsGS3oG05o9XRk0QqRWhaQAC_gADVp29CtoEYTAu-df_JAQ',
            'CAACAgIAAxkBAAEFB3pip3G96WKIpj7-WbYMK2JO2_V1xwACBAEAAladvQreBNF6Zmb3bCQE',
            'CAACAgIAAxkBAAEFB3hip3GgC4XNsOszN-qXtjzMGKfVRgAC9wADVp29CgtyJB1I9A0wJAQ',
            'CAACAgIAAxkBAAEFB4Rip3L9MK4MCQ_1l962Vy0YPtFTaQACGwADwDZPE329ioPLRE1qJAQ',
            'CAACAgIAAxkBAAEFB4Jip3L6vR-DoRlZBNwqxQzmzKybSAACHQADwDZPE17YptxBPd5IJAQ']


def reasons(date):
    url = ''
    match date:
        case 'today':
            url = 'https://prazdnikisegodnya.ru/'
        case 'tomorrow':
            url = 'https://prazdnikisegodnya.ru/zavtra/'
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    holidays = soup.find_all('span')
    text = ""
    count = 0
    row = "\n¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\n"
    for day in holidays:
        if '\n' not in day.text:
            count += 1
            text += str(count) + ". " + day.text + row
    return text


@bot.message_handler(commands=['info'])
def helper(message):
    _id = message.chat.id
    bot.send_message(_id, "Информация взята из электронного ресурса <b>prazdnikisegodnya.ru</b>", parse_mode="html")


@bot.message_handler(commands=['start'])
def start(message):
    _id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.add('Сегодня', 'Завтра')
    bot.send_message(_id, "Привет! Выбери день, чтобы узнать праздники", reply_markup=keyboard)


@bot.message_handler()
def check(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    _id = message.chat.id
    match message.text:
        case 'Сегодня':
            bot.send_message(_id, "Праздники сегодня:", parse_mode="html")
            bot.send_message(_id, reasons("today"), parse_mode="html")
        case 'Завтра':
            bot.send_message(_id, "Праздники завтра:", parse_mode="html")
            bot.send_message(_id, reasons("tomorrow"), parse_mode="html")
    bot.send_sticker(_id, stickers[random.randint(0, len(stickers) - 1)])


bot.polling(none_stop=True)
