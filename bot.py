import telebot
import os
from dotenv import load_dotenv
import openai_interface as oif
import requests
import json

load_dotenv()

# initialise bot
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


# Test bot online status
@bot.message_handler(commands=['ping'])
def net_check(message):
    bot.reply_to(message, "Pong!")


# Get weather of given region
@bot.message_handler(commands=['weather'])
def getweatherinfo(message):
    bot.reply_to(message, "Pong!")


# Use ChatGPT for responses
@bot.message_handler(func=lambda msg: True)
def chat_gpt_complete(message):
    bot.reply_to(message, oif.get_response(message.text))


bot.infinity_polling()
