#pip install aiohttp
#pip install mysql-connector-python
#pip install python-dotenv
#pip install python-telegram
# pip install "python_telegram_bot==12.4.2"

from telegram import ParseMode
import telebot
from telebot import types
import requests
from dotenv import load_dotenv
import os

load_dotenv()

bot = telebot.TeleBot(os.getenv("bot_api_key"))

geocoding_base_url = "https://maps.googleapis.com/maps/api/geocode/json"

user_choices = {
    "address": "Compartilhar endereço de entrega",
    "order": "Iniciar pedido",
    "confirm": "Sim",
    "deny": "Não"
}

reply_keyboard_buttons = [
    types.KeyboardButton(user_choices["address"], request_location=True),
    types.KeyboardButton(user_choices["order"])
]

inline_anwsers = [
    types.InlineKeyboardButton(text=user_choices["confirm"], callback_data="confirm"),
    types.InlineKeyboardButton(text=user_choices["deny"], callback_data="deny")
]

quantity = 0


user_reply_keyboard = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
user_reply_keyboard.add(*reply_keyboard_buttons)

inline_replies = types.InlineKeyboardMarkup(row_width=2)
inline_replies.add(*inline_anwsers)

# def initial_trigger(msg):
#     return True

@bot.message_handler(commands=['start'])
def send_welcome(msg):
    bot.reply_to(msg, "Olá! Vai um Pizza Botinho? Aqui o seu pedido é montado com apenas alguns cliques :)\n\nSelecione uma das opções abaixo", reply_markup=user_reply_keyboard)
    
@bot.message_handler(content_types=['location', 'text'])
def reply_main_choices(msg):
    
    if msg.location:

        latitude = msg.location.latitude
        longitude = msg.location.longitude     
        
        params = {
            "latlng": f"{latitude},{longitude}", 
            "key": os.getenv("geo_api_key")
        }
                
        response = requests.get(geocoding_base_url, params=params)
        data = response.json()
        
        if data["status"] == "OK":
            address = data["results"][0]["formatted_address"]
            bot.reply_to(msg, "Confirma o endereço: %s?" % address, reply_markup=inline_replies) #TODO: tratar callbacks em uma func separada
            pass
        else:
             bot.reply_to(msg, "error at get address from google api") #adicionar opção de inserir manualmente
             
@bot.message_handler(content_types=['service'])
def handle_service_message(msg):
    if msg.content_type == 'service':
        if msg.json['data']:
            produtos = msg.json['data']
            for produto in produtos:
                nome = produto.get('nome')
                quantidade = produto.get('quantidade')
                preco = produto.get('preco')
                
                print(produto)
                # Agora você pode processar esses dados como necessário
        
        
        
bot.polling()