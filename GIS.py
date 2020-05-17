import telebot
import pyowm
import csv
import time
from telebot import apihelper

apihelper.proxy = {
   'http':'current proxy'
}

owm = pyowm.OWM('token', language = "ru")

bot = telebot.TeleBot("token")


@bot.message_handler(content_types=['location'])

def send_ecco(message):
    global answer;
    global humidity;
    global temp;
    global wind;
    global windeg;
    global tdate;
    global pressure;
    global latitude;
    global longitude;
    global idd;
    global l;

    observation = owm.weather_at_coords(message.location.latitude, message.location.longitude)

    l = observation.get_location()
    w = observation.get_weather()
    humidity = w.get_humidity()
    temp = w.get_temperature('celsius')["temp"]
    wind = w.get_wind()["speed"]
    windeg = w.get_wind()["deg"]
    tdate = observation.get_reception_time(timeformat='iso')
    pressure = w.get_pressure()["press"] / 1.333
    latitude = str(message.location.latitude)
    longitude = str(message.location.longitude)

    answer = "Текущие метеоусловия в " + l.get_name() + "\n"
    answer += "Облачность: " + w.get_detailed_status() + "\n"
    answer += "Относительная влажность: "  + str(humidity) + "%" + "\n"
    answer += "Температура воздуха: " + str(temp) + "\n"
    answer += "Скорость ветра: " + str(wind) + " м/сек." + "\n"
    answer += "Направление ветра: " + str(windeg) + " град." + "\n"
    answer += "Атмосферное давление: " + str(round(pressure, 2)) + " мм. рт. столба" + "\n"
    answer += "Дата и время наблюдения: " + str(tdate) + "\n"
    answer += "Координаты места: " + str(round(message.location.latitude, 2)) + ' ; ' + str(round(message.location.longitude, 2))

    bot.send_message(message.from_user.id, 'Опишите запах и его интенсивность по шкале от 1 до 5. \n Например: "Запах газа, 3"');
    bot.register_next_step_handler(message, description)

def description(message):
    global descr;
    descr = message.text
    

    bot.send_message(message.chat.id, 'Спасибо! Наблюдение принято.')
    time.sleep(3)
    bot.send_message(message.chat.id, answer)

    with open('log.csv', 'a', newline='', encoding='utf-8') as csvfile:
            datawriter = csv.writer(csvfile, delimiter='&', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            datawriter.writerow([str(tdate)]+[latitude]+[longitude]+[str(temp)]+[str(wind)]+[str(windeg)]+[str(humidity)]+[str(round(pressure, 2))]+[str(descr)])



@bot.message_handler(content_types=['text'])
def send_back(message):

    bot.send_message(message.chat.id, 'Для создания отчета, снчала отправьте текущие координаты вашего местоположения.')
    time.sleep(1.5)
    bot.send_message(message.chat.id, 'Нажмите 📎, затем Location.')


bot.infinity_polling(True)
