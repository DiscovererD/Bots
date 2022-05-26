import telebot
import requests
from bs4 import BeautifulSoup as BS

bot = telebot.TeleBot('')

@bot.message_handler(commands = ['start'])
def start(message):
	bot.send_message(message.chat.id, '<b>Hi! </b>I am the professional chemistrty bot. Write me an equation and I will solve it!' parse_mode = 'html')

@bot.message_handler()
def get_user_text(message):
	eq = message.text	
	s = requests.Session()
	auth_html = s.get('https://chemequations.com/en/')
	payload = {
		's':f'{eq}'
	}
	answ = s.post("https://chemequations.com/en/", data = payload)
	html = BS(answ.content, "html.parser")
	res = html.find('h1', {'class' : 'equation main-equation well'}).text.strip()
	bot.send_message(message.chat.id, res, parse_mode = 'html')

bot.polling(none_stop = True)