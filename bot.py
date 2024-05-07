#pip install aiohttp
# pip install mysql-connector-python

import telebot
from telebot import types
# import aiohttp
# from telebot.async_telebot import AsyncTeleBot
# import asyncio
import requests

#db
import mysql.connector

db_config = {
    "user": "root",
    "password": "admin",
    "host": "localhost",
    "port": 33061
}

mydb = mysql.connector.connect(**db_config)

bot_api_key = "6665864422:AAGgCRdfPMdghuYj62uVuzRA7Cwccru6AAo"
bot = telebot.TeleBot(bot_api_key)

geocoding_base_url = "https://maps.googleapis.com/maps/api/geocode/json"
geo_api_key = "AIzaSyDW2XKp1OWuoIPfEzLmiMW79fG9e1jGBuo"

user_choices = {
    "address": "Cadastrar meu endereço",
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
    bot.reply_to(msg, "Olá! Vai um Pizza Botinho? Com ele você pode realizar pedidos facilmente com apenas alguns cliques\n\nSelecione a opção que deseja fazer, caso seja seu primeiro pedido conosco, recomendamos cadastrar seu endereço antes para lembrarmos futuramente :)", reply_markup=user_keyboard)
    
@bot.message_handler(content_types=['location', 'text'])
def reply_main_choices(msg):
    
    if msg.location:

        latitude = msg.location.latitude
        longitude = msg.location.longitude     
        
        params = {
            "latlng": f"{latitude},{longitude}", #TODO: Pesquisar sobre fstrings depois
            "key": geo_api_key
        }
                
        response = requests.get(geocoding_base_url, params=params)
        data = response.json()
        
        if data["status"] == "OK":
            address = data["results"][0]["formatted_address"]
            bot.reply_to(msg, "Seu endereço é: %s" % address)
        else:
             bot.reply_to(msg, "error at get address from google api")
            
bot.polling()