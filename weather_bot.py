import telebot
import sys
import requests
import json
import schedule
import time
import emoji
import traceback
from apscheduler.schedulers.blocking import BlockingScheduler

DEV_API_KEY = "44db6a862fba0b067b1930da0d769e98"
TOKEN = '213675554:AAEHHFkB-NCFt0evRhfoodeL3SOIIEfDGNQ'
dest = '@clima_rio'
shut_down_alert = '@shut_down_clima_rio'

bot = telebot.TeleBot(TOKEN)
sched = BlockingScheduler()

def kelvin_to_celsius(kelvin):
    return ("%.1f" % (kelvin - 273) )

def job():
    try:
        city = "rio de janeiro"
        country = "br"
        url = "http://api.openweathermap.org/data/2.5/weather?q={0},{1}&lang=pt&appid={2}".format(city, country, DEV_API_KEY)
        response = requests.request("GET", url)
        data = json.loads(response.text)
        list_of_weathers = data['weather']
        current_weather = list_of_weathers[0]
        main_current = current_weather['main']

        main = data['main']

        # get description
        description = current_weather['description']
        description = description[:1].upper() + description[1:]

        # emojis
        cloud = ':cloud:'
        sun_behind_cloud = ':sun_behind_cloud:'
        sun = ':black_sun_with_rays:'
        sun_with_cloud_and_rain = ':white_sun_behind_cloud_with_rain:'
        rain = ':cloud_with_rain:'

        emoji_to_show = sun # default is the sun

        humidity = main['humidity']
        temp = main['temp']
        temp_min = kelvin_to_celsius(main['temp_min'])
        temp_max = kelvin_to_celsius(main['temp_max'])


        if main_current == 'Clouds':
            emoji_to_show = ':cloud:'
        else:
            # send sun (default) and send message for me
            bot.send_message(shut_down_alert, "description to add: {0}".format(main_current))

        bot.send_message(dest, emoji.emojize("{0} - {1} \nTemperatura maxima: {2} C\nTemperatura minima: {3} C\nUmidade de {4}%\n\n==============\nCreated by @JGabrielFreitas\nPowered by OpenWeather API".format(emoji_to_show, description, temp_max, temp_min, humidity))) # dest and msg
        # print emoji.emojize("{0} - {1} \nTemperatura maxima: {2} C\nTemperatura minima: {3} C\nUmidade de {4}%\n\n==============\nCreated by @JGabrielFreitas\nPowered by OpenWeather API".format(emoji_to_show, description, temp_max, temp_min, humidity))
    except:
        bot.send_message(shut_down_alert, "Dude, your bot is down...:\n\n{0}".format(traceback.format_exc()))

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')
    job()


# run jobs
# schedule.every().hour.do(job)
# schedule.every(1).minutes.do(job)
#
# while True:
#     schedule.run_pending()
    # time.sleep(1)
# job()
sched.start()
