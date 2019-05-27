import telebot
from telebot import types
from telebot import apihelper
# import logging
import sys
import os
import time
import requests
import gdown


# proxy = 'https://KgaTRs:8h7HqG@138.59.206.204:9491'
server = 'https://api.telegram.org'
proxy_list = 'https://drive.google.com/uc?id=1YIU9CyG6PJhojiam13znjC5migGxVEJj'
proxy_list_file = 'proxylist.txt'
log_file = "error.log"


# token = '799646588:AAG6_o_kkcVMIOzLBwCAMj_52YuCK2QOirY'
chatId = 228534214


door = True  # дверь закрыта
window1 = True  # окно 1 закрыто
window2 = True  # окно 2 закрыто
alarmStatus = False  # статус сигнализации, True - активна, False - неактивна


# Функции обработки прерываний


def load_proxy_list():
    try:
        f = open(os.path.abspath(proxy_list_file), "r")
        return f.read()
    except Exception:
        log_error(time.strftime("%d.%m.%Y %H:%M:%S") +
                  " Невозможно прочитать файл proxylist.txt!\n")


def alarm(channel):
    global door, window1, window2, alarmStatus
    if not(door and window1 and window2):
        bot.send_message(chatId, "ВНИМАНИЕ! Произошло вскрытие:")
    pass


def info():
    global door, window1, window2, alarmStatus
    i = []
    if(alarmStatus):
        i.append('Сигнализация активна\n')
    else:
        i.append('Сигнализация отключена\n')
    if(door):
        i.append('Дверь закрыта\n')
    else:
        i.append('Дверь открыта\n')
    if(window1):
        i.append('Окно в спальне закрыто\n')
    else:
        i.append('Окно в спальне открыто\n')
    if(window2):
        i.append('Окно в зале закрыто\n')
    else:
        i.append('Окно в зале открыто\n')
    return i


def set_alarm():
    global door, window1, window2, alarmStatus
    if (door and window1 and window2):
        alarmStatus = True
        return True
    else:
        return False


def unset_alarm():
    global alarmStatus
    alarmStatus = False
    return True


def generate_menu(alarmStatus=None):
    mainmenu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    itembtn1 = types.KeyboardButton('Состояние дома')
    if(alarmStatus):
        itembtn2 = types.KeyboardButton('Снять с сигнализации')
    else:
        itembtn2 = types.KeyboardButton('Поставить на сигнализацию')
    itembtn3 = types.KeyboardButton('Включить отопление')
    mainmenu.add(itembtn1, itembtn2, itembtn3)
    return mainmenu


def log_error(e):
    try:
        f = open(os.path.abspath(log_file), "a")
        f.write(e)
        f.close()
    except Exception as e:
        print(e)


def check_inet():
    proxies = {'https': load_proxy_list()}
    try:
        r = requests.get(server, timeout=5, proxies=proxies)
        r.raise_for_status()
    except Exception as err:
        print(('Other error occurred:{err}').format(err=err))
        log_error(time.strftime("%d.%m.%Y %H:%M:%S") +
                  " Нет интернет соединения!\n")
        output = 'proxylist.txt'
        try:
            gdown.download(proxy_list, output, quiet=False)
            log_error(time.strftime("%d.%m.%Y %H:%M:%S") +
                      " Список прокси обновлен!\n")
        except Exception:
            log_error(time.strftime("%d.%m.%Y %H:%M:%S") +
                      " Невозможно скачать список прокси с облака!\n")


# r = check_inet(proxy)
# print(r)

logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def send_menu(message):
    bot.send_message(message.chat.id, 'Выберите пункт меню:',
                     reply_markup=generate_menu())


@bot.message_handler(content_types=['text'])
def send_message(message):
    global door, window1, window2, alarmStatus

    if(message.text == 'Состояние дома'):
        info_t = info()
        t = ''
        for i in info_t:
            t = t + i
        info_home = t + 'Температура в доме: 12 °С\nТемпература на улице: 2 °С\nСостояние АКБ: 12,3 В'
        bot.send_message(message.chat.id, info_home,
                         reply_markup=generate_menu(alarmStatus))
        print(message.chat.id)

    if(message.text == 'Поставить на сигнализацию'):
        if (set_alarm()):
            bot.send_message(message.chat.id, 'Сигнализация активна!',
                             reply_markup=generate_menu(alarmStatus))
        else:
            bot.send_message(message.chat.id, 'Невозможно поставить на сигнализацию\n',
                             reply_markup=generate_menu(alarmStatus))

    if(message.text == 'Снять с сигнализации'):
        if unset_alarm():
            bot.send_message(message.chat.id, 'Сигнализация не активна!',
                             reply_markup=generate_menu(alarmStatus))

    if(message.text == 'Включить отопление'):
        window1 = False
        alarm(1)
        bot.send_message(message.chat.id, 'Отопление включено!',
                         reply_markup=generate_menu())


def main():
    while True:
        try:
            apihelper.proxy = {'https': load_proxy_list()}
            bot.polling(none_stop=True)
            time.sleep(1)
        except Exception:
            check_inet()
            time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Exit programm')
        sys.exit(0)
