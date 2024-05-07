#pip install aiohttp
#pip install mysql-connector-python
#pip install python-dotenv

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
    "menu": "Ver cardápio",
    "order": "Iniciar pedido"
}

keyboard_buttons = [
    types.KeyboardButton(user_choices["address"], request_location=True),
    types.KeyboardButton(user_choices["menu"]),
    types.KeyboardButton(user_choices["order"])
]

user_keyboard = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
user_keyboard.add(*keyboard_buttons)

# def initial_trigger(msg):
#     return True

@bot.message_handler(commands=['start'])
def send_welcome(msg):
    bot.reply_to(msg, "Olá! Vai um Pizza Botinho? Aqui o seu pedido é montado com apenas alguns cliques :)\n\nSelecione a opção que deseja fazer", reply_markup=user_keyboard)
    
@bot.message_handler(content_types=['location', 'text'])
def reply_main_choices(msg):
    
    if msg.location:

        latitude = msg.location.latitude
        longitude = msg.location.longitude     
        
        params = {
            "latlng": f"{latitude},{longitude}", #TODO: Pesquisar sobre fstrings depois
            "key": os.getenv("geo_api_key")
        }
                
        response = requests.get(geocoding_base_url, params=params)
        data = response.json()
        
        if data["status"] == "OK":
            address = data["results"][0]["formatted_address"]
            bot.reply_to(msg, "Seu endereço é: %s" % address)
        else:
             bot.reply_to(msg, "error at get address from google api")
             
    elif msg.text == user_choices["menu"]:
        bot.reply_to(msg, "Ótimo! Vou lhe passar o cardápio")
        
        for pizza in pizzas:
            
            sabor = pizza["flavor"]
            preco = pizza["price"]
            
            cover_url = get_pizza_ilustration(sabor)
            menu_text = f":pizza: **Sabor**: {sabor}\n\n**Preço:** 20"
            
            bot.send_message(msg.chat.id, menu_text, parse_mode='MarkdownV2')
            
            # with open(cover_url, "rb") as photo:
            #     bot.send_photo(msg.chat.id, photo, caption=f"Pizza de {sabor}")
            
bot.polling()