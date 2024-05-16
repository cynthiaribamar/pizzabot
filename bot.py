#pip install aiohttp
#pip install python-dotenv
#pip install python-telegram
# pip install "python_telegram_bot==12.4.2"

from telegram import ParseMode
import telebot
from telebot import types
import requests
from dotenv import load_dotenv
import os
from json import loads

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
    types.KeyboardButton(user_choices["order"], web_app=types.WebAppInfo("https://cynthiaribamar.github.io/pizzabot/index.html"))
]

inline_anwsers = [
    types.InlineKeyboardButton(text=user_choices["confirm"], callback_data="confirm"),
    types.InlineKeyboardButton(text=user_choices["deny"], callback_data="deny")
]

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
             bot.reply_to(msg, "Hmm peço desculpas, ocorreu um erro ao buscar o seu endereço.") #adicionar opção de inserir manualmente


@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(msg):
    
    order = "<b>RESUMO DO PEDIDO</b>\n\n"
    data = msg.web_app_data.data
    pedidos = loads(data);
    # total = sum(pedidos[""])
    
    for pedido in pedidos:
        
        qtd = pedido["quantidade"]
        pizza = pedido["pizza"]
        preco = pedido["preco"]   

        order+= f"{qtd}x {pizza} {qtd}\n"
        
    # print(data)
    # print(type(data))
    # print(pedidos)
    # print (type(pedidos))
    print(data)
    # bot.reply_to(msg, f"{order}", parse_mode=ParseMode.HTML)
        
##caption=f"<b>Sabor:</b>  {sabor}\n<b>Preço:</b> R${preco}", parse_mode=ParseMode.HTML
        
        
        
bot.polling()