import telebot
from telebot import types
import logging

token = '799646588:AAFiCOLFzOaTITLhekOBgUs1TMm8pVIRU9A'
chatId = 228534214


door = True #дверь закрыта
window1 = True #окно 1 закрыто
window2 = True #окно 2 закрыто
alarmStatus = False #статус сигнализации, True - активна, False - неактивна

i = {
	'alarmStatus': [False, ""],
	'door': [True, "Дверь открыта"],
	}


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
bot = telebot.TeleBot(token)

#u = bot.get_me()
#print(u)


# Функции обработки прерываний
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


@bot.message_handler(commands=['start', 'help'])
def send_menu(message):
	bot.send_message(message.chat.id, 'Выберите пункт меню:', reply_markup=generate_menu())

@bot.message_handler(content_types=['text'])
def send_message(message):
	global door, window1, window2, alarmStatus
	
	if(message.text == 'Состояние дома'):
		info_t = info()
		t = ''
		for i in info_t: t = t+i
		info_home = t+'Температура в доме: 12 °С\nТемпература на улице: 2 °С\nСостояние АКБ: 12,3 В'
		bot.send_message(message.chat.id, info_home, reply_markup=generate_menu(alarmStatus))
		print(message.chat.id)
	
	if(message.text == 'Поставить на сигнализацию'):
		if (door and window1 and window2):
			alarmStatus = True
			bot.send_message(message.chat.id, 'Сигнализация активна!', reply_markup=generate_menu(alarmStatus))
		else:
			bot.send_message(message.chat.id, 'Невозможно поставить на сигнализацию\n', reply_markup=generate_menu(alarmStatus))	
	
	if(message.text == 'Снять с сигнализации'):
		alarmStatus = False
		bot.send_message(message.chat.id, 'Сигнализация не активна!', reply_markup=generate_menu(alarmStatus))		
	
	if(message.text == 'Включить отопление'):
		window1 = False
		alarm(1)
		bot.send_message(message.chat.id, 'Отопление включено!', reply_markup=generate_menu())						

def generate_menu(alarmStatus=None):
	mainmenu = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
	itembtn1 = types.KeyboardButton('Состояние дома')
	if(alarmStatus):
		itembtn2 = types.KeyboardButton('Снять с сигнализации')
	else:
		itembtn2 = types.KeyboardButton('Поставить на сигнализацию')
	itembtn3 = types.KeyboardButton('Включить отопление')
	mainmenu.add(itembtn1, itembtn2, itembtn3)
	return mainmenu


bot.polling()