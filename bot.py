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
from utils import get_pizza_ilustration
from pizzas import pizzas

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

buy_buttons = [
    types.InlineKeyboardButton(text="-", callback_data="add"),
    types.InlineKeyboardButton(text=f"{quantity}", callback_data="qt"),
    types.InlineKeyboardButton(text="+", callback_data="remove")
]

user_reply_keyboard = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
user_reply_keyboard.add(*reply_keyboard_buttons)

inline_replies = types.InlineKeyboardMarkup(row_width=2)
inline_replies.add(*inline_anwsers)

buy_markup = types.InlineKeyboardMarkup(row_width=3)
buy_markup.add(*buy_buttons)
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
             
    elif msg.text == user_choices["order"]:
        bot.reply_to(msg, "Ótimo! Vou lhe passar o cardápio, selecione a quantidade que deseja de cada sabor, para fechar o pedido clique no botão que aparecerá ao fim dos itens")
        
        for pizza in pizzas:
            
            sabor = pizza["flavor"]
            preco = pizza["price"]
            
            cover = get_pizza_ilustration(sabor)
            bot.send_photo(msg.chat.id, cover, caption=f"<b>Sabor:</b>  {sabor}\n<b>Preço:</b> R${preco}", parse_mode=ParseMode.HTML, reply_markup=buy_markup)  
            
    else:
        bot.reply_to(msg, "Por favor, selecione uma das duas opções")
        
@bot.callback_query_handler(func=lambda call:True)
def handle_callbacks(call):
        if call.data == "confirm":
            bot.send_message(call.message.chat.id, "Ótimo! Daqui alguns minutos seu pedido chegará até você nesse endereço ;)")
        
        if call.data == "add":
            quantity = quantity + 1
        
        
bot.polling()