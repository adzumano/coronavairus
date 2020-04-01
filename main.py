import telebot
from telebot import types
import COVID19Py
import time
import constants

bot = telebot.TeleBot(constants.TOKEN)
covid19 = COVID19Py.COVID19()


@bot.message_handler(commands=['start'])
def start(message):

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
	btn1 = types.KeyboardButton('Во всём мире')
	btn2 = types.KeyboardButton('Украина')
	btn3 = types.KeyboardButton('Россия')
	btn4 = types.KeyboardButton('Беларусь')
	btn5 = types.KeyboardButton('Америка')
	btn6 = types.KeyboardButton('Казахстан')
	btn7 = types.KeyboardButton('Италия')
	btn8 = types.KeyboardButton('Франция')

	markup.add(btn1, btn2, btn3, btn4,btn5, btn6, btn7, btn8)

	send_message = "<b><u>Привет %s!</u></b>\nЧтобы узнать данные про коронавируса напишите название страны, например:\n<u>США, Украина, Россия</u> и так далее" % (message.from_user.first_name)
	bot.send_message(message.chat.id, send_message, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def mess(message):

    final_message = ""
    get_message_bot = message.text.strip().lower()
    if get_message_bot == "сша" or get_message_bot == "usa":
        location = covid19.getLocationByCountryCode("US")
    elif get_message_bot == "украина" or get_message_bot == "ua" or get_message_bot == "ukraine":
        location = covid19.getLocationByCountryCode("UA")
    elif get_message_bot == "россия" or get_message_bot == "russia" or get_message_bot == "ru":
        location = covid19.getLocationByCountryCode("RU")
    elif get_message_bot == "беларусь" or get_message_bot == "belarus" or get_message_bot == "by":
        location = covid19.getLocationByCountryCode("BY")
    elif get_message_bot == "казакхстан" or get_message_bot == "kazakhstan" or get_message_bot == "kz":
        location = covid19.getLocationByCountryCode("KZ")
    elif get_message_bot == "италия" or get_message_bot == "italy" or get_message_bot == "it":
        location = covid19.getLocationByCountryCode("IT")
    elif get_message_bot == "франция" or get_message_bot == "france" or get_message_bot == "fr":
        location = covid19.getLocationByCountryCode("FR")
    elif get_message_bot == "германия" or get_message_bot == "germany" or get_message_bot == "de":
        location = covid19.getLocationByCountryCode("DE")
    elif get_message_bot == "япония" or get_message_bot == "japan" or get_message_bot == "jp":
        location = covid19.getLocationByCountryCode("JP")
    else:
        location = covid19.getLatest()
    # final_message = "<u>Данные по всему миру:</u>\n<b>Заболевших: </b>%s\n<b>Сметрей: </b>%s" % (location['confirmed'],location['deaths'])
    final_message = f"{location}"
    if final_message == "":
        date = location[0]['last_updated'].split("T")
        time = date[1].split(".")
        final_message = "<u>Данные по стране:</u><br>Население: %s%s<br>\nПоследнее обновление: %s<br>Последние данные:<br><b>\nЗаболевших: %s</b><br><b>Сметрей: %s</b>\n" % (location[0]['country_population'],date[0],time[0],location[0]['latest']['confirmed'],location[0]['latest']['deaths'])

    bot.send_message(message.chat.id, final_message, parse_mode='html')

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(15)