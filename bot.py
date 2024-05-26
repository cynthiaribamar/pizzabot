#pip install python-dotenv

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
}

reply_keyboard_buttons = [
    types.KeyboardButton(user_choices["address"], request_location=True),
    types.KeyboardButton(user_choices["order"], web_app=types.WebAppInfo("https://cynthiaribamar.github.io/pizzabot/index.html"))
]

markup = types.ForceReply(selective=False)

def dynamic_keyboard(btn):
    user_reply = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    user_reply.add(btn)
    return user_reply

# def initial_trigger(msg):
#     return True

@bot.message_handler(commands=['start'])
def send_welcome(msg):
    dynamic_keyboard('welcome')
    bot.reply_to(msg, f"Olá! Vai um Pizza Botinho? Aqui o seu pedido é montado com apenas alguns cliques :)\n\nClique em <b>{user_choices['order']}</b> para acessar nosso cardápio!", reply_markup=dynamic_keyboard(reply_keyboard_buttons[1]), parse_mode=ParseMode.HTML)

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(msg):
    
    order = "<b>RESUMO DO PEDIDO</b>\n\n"
    data = msg.web_app_data.data
    pedidos = loads(data);
    total = [];
    
    for pedido in pedidos:
        
        qtd = int(pedido["quantidade"])
        pizza = pedido["pizza"]
        preco = int(pedido["preco"]) 
        final_value = (preco * qtd)
        total.append(final_value)

        order+= f"## {qtd}x     {pizza} R${qtd * preco}\n"
        
    bot.reply_to(msg, f"{order}\n\n<b>TOTAL DO PEDIDO: R${sum(total)}</b>", parse_mode=ParseMode.HTML)
    
    dynamic_keyboard('address')
    bot.send_message(msg.chat.id, f"Ótimo, estamos com o seu pedido! Agora vou pedir para que nos informe o endereço de entrega, basta clicar em <b>{user_choices['address']}</b>", reply_markup=dynamic_keyboard(reply_keyboard_buttons[0]), parse_mode=ParseMode.HTML)

@bot.message_handler(content_types=['location', 'text'])
def get_delivery_address(msg):
    
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
            bot.reply_to(msg, "Ótimo! Daqui alguns minutos seu pedido chegará até você no endereço %s \n\nObrigada por pedir conosco, até mais!" % address) 
            bot.send_message(msg.chat.id, "Se quiser iniciar um pedido, digite /start")
            pass
        else:
            bot.reply_to(msg, "Hmm peço desculpas, ocorreu um erro ao buscar o seu endereço.")
                 
        
bot.polling()