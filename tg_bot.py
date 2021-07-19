# Подлкючаем библиотеку requests
import requests
# Подключаем нужные для бота модули из библиотеки telegram.ext
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pandas as pd

df = pd.read_csv('cian_advert_db.csv')
# это наша функция для получения адреса по координатам. С ней мы знакомы.


def get_advert(city):
    try:
        indexes_match_queries = df.apply(
            lambda row: str(city).lower() in str(row['City']).lower(),
            axis=1,
        )
        df1 = df[indexes_match_queries]
        # indexes_match_queries1 = df1.apply(
        #     lambda row: str(metro).lower() in str(row['Nearest metro']).lower(),
        #     axis=1,
        # )
        # df2 = df1[indexes_match_queries1]
        # indexes_match_queries1 = df2.apply(
        #     lambda row: str(rooms).lower() in str(row['Title']).lower(),
        #     axis=1,
        # )
        # df3 = df2[indexes_match_queries1]
        return str(df1.sample(1)['Link'])

    except:
        return 'К сожалению, такая квартира не нашлась('


# Эта функция будет использоваться когда человек первый нажал в боте START
def start(update, context):
    update.message.reply_text('Давайте найдем вам жилье! Москва или Питер?')


def city_scr(update, context):
    city = update.message.text
    update.message.reply_text(get_advert(city))


def metro_scr(update, context):
    metro = update.message.text
    update.message.reply_text('Отлично, а 1-, 2- или 3- комнатную?')


def rooms_scr(update, context):
    rooms = update.message.text


# Это основная функция, где запускается наш бот
def main():
    # создаем бота и указываем его токен
    updater = Updater("1914822734:AAF3WmOibb4bIoIYC3hNCyFwkr86xur2JHI", use_context=True)
    # создаем регистратор событий, который будет понимать, что сделал пользователь и на какую функцию надо переключиться.
    dispatcher = updater.dispatcher

    # регистрируем команду /start и говорим, что после нее надо использовать функцию def start
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, city_scr))
    # dispatcher.add_handler(MessageHandler(Filters.text, metro_scr))
    # dispatcher.add_handler(MessageHandler(Filters.text, rooms_scr))
    # print(get_advert(city, metro, rooms))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    # запускаем функцию def main
    main()
