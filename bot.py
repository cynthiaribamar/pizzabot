#pip install aiohttp

import telebot
from telebot import types
import aiohttp
# from telebot.async_telebot import AsyncTeleBot
# import asyncio

api_key = "6665864422:AAGgCRdfPMdghuYj62uVuzRA7Cwccru6AAo"

bot = telebot.TeleBot(api_key)

user_choices = {
    "address": 'Cadastrar meu endereço',
    "menu": 'Ver cardápio',
    "order": 'Iniciar pedido'
}

keyboard_buttons = [
    types.InlineKeyboardButton(text=user_choices["address"], callback_data="address"),
    types.InlineKeyboardButton(text=user_choices["menu"], callback_data="menu"),
    types.InlineKeyboardButton(text=user_choices["order"], callback_data="order", switch_inline_query_current_chat="pqp")
]

inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
inline_keyboard.add(*keyboard_buttons)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(msg):
    bot.reply_to(msg, "Olá! Vai um Pizza Botinho? Com ele você pode realizar pedidos facilmente com apenas alguns cliques\n\nSelecione a opção que deseja fazer, caso seja seu primeiro pedido conosco, recomendamos cadastrar seu endereço antes para lembrarmos futuramente :)", reply_markup=inline_keyboard)

# @bot.message_handler(func=lambda msg: True)
# async def echo_message(msg):
#     await bot.reply_to(msg, msg.text)

# @bot.callback_query_handler(func=lambda call: True)
# async def user_callback(call):
#     chat_id = call.message.id

# asyncio.run(bot.polling())
bot.polling()