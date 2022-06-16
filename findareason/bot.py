import telebot
import requests
from bs4 import BeautifulSoup
import random

token = '5521967872:AAEpu7Mm33L7yphxR4DtIxtvVB4vDE46BE4'
bot = telebot.TeleBot(token)

# IP анимированных стикеров
stickers = ['CAACAgIAAxkBAAEFB35ip3HOcsGS3oG05o9XRk0QqRWhaQAC_gADVp29CtoEYTAu-df_JAQ',
            'CAACAgIAAxkBAAEFB3pip3G96WKIpj7-WbYMK2JO2_V1xwACBAEAAladvQreBNF6Zmb3bCQE',
            'CAACAgIAAxkBAAEFB3hip3GgC4XNsOszN-qXtjzMGKfVRgAC9wADVp29CgtyJB1I9A0wJAQ',
            'CAACAgIAAxkBAAEFB4Rip3L9MK4MCQ_1l962Vy0YPtFTaQACGwADwDZPE329ioPLRE1qJAQ',
            'CAACAgIAAxkBAAEFB4Jip3L6vR-DoRlZBNwqxQzmzKybSAACHQADwDZPE17YptxBPd5IJAQ']


def generator(message):
    """
    Генерация рандомного тоста из файла tosts.txt
    :param message:
        Запрос пользователя
    """
    with open("tosts.txt", "r", encoding="utf8") as f:
        tosts = f.read().split('\n')
    bot.send_message(message.chat.id, tosts[random.randint(0, len(tosts)-1)])


def reasons(date):
    """
    Парсинг сайта, url в соответствии с датой
    :param date:str
        Значение даты (сегодня 'today'/завтра 'tommorow')
    :return:
        Возврат списка единым текстом с междустрочными разделителями
    """
    url = ''
    match date:
        case 'today':
            url = 'https://prazdnikisegodnya.ru/'
        case 'tomorrow':
            url = 'https://prazdnikisegodnya.ru/zavtra/'
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    holidays = soup.find_all('span')
    text = ""
    count = 0  # Порядковый номер в списке
    row = "\n¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\n"  # Разделитель
    for day in holidays:
        if '\n' not in day.text:
            count += 1
            text += str(count) + ". " + day.text + row
    return text


@bot.message_handler(commands=['info'])
def helper(message):
    """
    Вывод информации по info.
    :param message:
        Запрос пользователя командой /info
    """
    _id = message.chat.id
    bot.send_message(_id, "Информация взята из электронного ресурса <b>prazdnikisegodnya.ru</b>", parse_mode="html")


@bot.message_handler(commands=['start'])
def start(message):
    """
    Установка reply-кнопок при первом взаимодействии командой start
    :param message:
        Сообщение пользователя /start
    """
    _id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(True)  # Подключение reply-кнопок
    keyboard.add('Сегодня', 'Завтра')
    keyboard.add('Рандомный тост')
    bot.send_message(_id, "Привет! Выбери день, чтобы узнать праздники", reply_markup=keyboard)


@bot.message_handler()
def check(message):
    """
    Обработка запроса пользователя, вывод списка по дате
    :param message:
        Выбор пользователя (нажатие reply-кнопки)
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    _id = message.chat.id
    sticker = stickers[random.randint(0, len(stickers) - 1)]
    match message.text:
        case 'Сегодня':
            bot.send_message(_id, "Праздники сегодня:")
            bot.send_message(_id, reasons("today"))
            #  Отправка стикера из коллекции
            bot.send_sticker(_id, sticker)
        case 'Завтра':
            bot.send_message(_id, "Праздники завтра:")
            bot.send_message(_id, reasons("tomorrow"))
            #  Отправка стикера из коллекции
            bot.send_sticker(_id, sticker)
        case 'Рандомный тост':
            cheers = 'CAACAgIAAxkBAAEFCaliqH9myHORoHE7h-_d1gQma6WFLAACSgIAAladvQrJasZoYBh68CQE'
            #  Генерация тоста из списка
            generator(message)
            bot.send_sticker(_id, cheers)
        case _:
            dont_get(message)


@bot.message_handler(content_types=["audio", "document", "photo", "sticker", "video", "video_note",
                                    "voice", "location", "contact"])
def dont_get(message):
    """
    Обработка сообщения или других файлов
    :param message:
        Запросы помимо кнопок
    """
    _id = message.chat.id
    ans = 'CAACAgIAAxkBAAEFCLVip8Ks7sndBPTyvMA7Q3Jq-MifQwACGAADwDZPE9b6J7-cahj4JAQ'
    bot.send_sticker(_id, ans)
    bot.send_message(_id, "Я тебя не понимаю :(\nЛучше нажми на кнопку!")


#  Запуск бота
bot.polling(none_stop=True)
