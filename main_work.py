import sqlite3 
import telebot 
from db_test import db
from keyboa.keyboard import Keyboa
import json

TOKEN = "5600063134:AAF4AYzjo14X-PGBx955a4x9zdaT8l_MhbE"
bot = telebot.TeleBot(TOKEN)
URL = 'https://api.telegram.org/bot'

loc = 0
render_array = ['14', '11', '12', '13', '15', '1', '17', '16', '22', '27', '32', '40', '46', '49', '55', '56', '60', '62', '58', '59', '60']
role_array = ['1', '11', '12', '13', '14', '15', '16']
community_array = ['55', '56', '57', '58', '59', '60']
resp = ['17', '22', '27', '32', '40', '46', '49']

@bot.message_handler(commands=['start', 'command1'])
def start_message(message):
	if db.get_user(message.chat.id) == []:
		bot.delete_message(message.chat.id, message.message_id)
		mess = db.get_node(loc)
		# print(mess)
		menu = Keyboa(items=json.loads(mess[0]['name']), items_in_row=mess[0]['count_in_row'])
		bot.send_message(message.chat.id, mess[0]['text'], reply_markup=menu(), parse_mode='Markdown')
		db.write_user(message.chat.id, loc)
	else:
		# print(db.get_user(message.chat.id))
		bot.delete_message(message.chat.id, message.message_id)



def render(id_user, id_outgo, node, call):	
	mess = db.get_node(node)
	role = db.get_user(id_user)[0]['role']
	print(role)
	before_node = db.get_user(id_user)[0]['id_last_connections']
	# db.update_user(call.message.chat.id, id_last_connections=node)
	js = json.loads(mess[0]['name'])

	menu = Keyboa(items=js, items_in_row=int(mess[0]['count_in_row']))
	
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mess[0]['text'], reply_markup=menu(), parse_mode="Markdown")

# @bot.callback_query_handler(func=lambda call: call in )

# @bot.callback_query_handler(func=lambda call: call == )
# def quiz()

@bot.callback_query_handler(func=lambda call: call.data == 'it')
def company(call):
	id_last_connections = db.get_user(call.message.chat.id)[0]['id_last_connections']
	# print(id_last_connections)
	render(call.message.chat.id,0, id_last_connections, call)
	
@bot.message_handler(commands=['restart'])
def restart(message):
	# bot.delete_message(message.chat.id, message.message_id)	
	db.delete_user(message.chat.id)
	start_message(message)
	# bot.send_message(message.chat.id, '/start', parse_mode='Markdown')




@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	# print(call.message.chat.id)
	# print(call.data)
	try:
		f = call.data
		print(f in role_array)
		if f in role_array:
			db.update_user(tg_name=call.message.chat.id, id_last_connections=call.data, role=call.data)
	except:
		db.update_user(tg_name=call.message.chat.id, id_last_connections=call.data)
		print('Not to int')
	# print(call.message.chat.id)
	user = db.get_user(tg_name=call.message.chat.id)
	# print(user)
	render(user[0]['tg_name'], user[0]['id_last_connections'], int(call.data), call)

# call.data == '1' or call.data == '2'
bot.polling(none_stop=True)
