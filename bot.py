#!/usr/bin/python3
import telebot
import os
from dotenv import load_dotenv
import openai_interface as oif
import requests
import json
from telegram.ext import *
import logging

load_dotenv()

# initialise bot
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

oif.init_msg = """
You are a conversational AI Chatbot specialising in positive user interaction. Pretend to be human wherever and whenever possible.

If you are faced with a question you cannot or are not allowed to answer, reply as a human would.

If asked about events outside your knowledge cutoff, or about recent events, just say that you don't know. If the content asked violates OpenAI policy, just simply decline to answer the question, as a human.
"""


# setting up logging
logging.basicConfig(filename="messages.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Test bot online status
@bot.message_handler(commands=['ping'])
def net_check(message):
    bot.reply_to(message, "Pong!")
    logger.info(f'''<{message.from_user.username}>: {message.text}''')


# Get weather of given region
@bot.message_handler(commands=['weather'])
def getweatherinfo(message):
    bot.reply_to(message, "Coming Soon!")
    logger.info(f'''<{message.from_user.username}>: {message.text}''')


@bot.message_handler(commands=['clearchat'])
def clearchat(message):
    oif.messages = []
    bot.reply_to(message, 'Cleared Chat')
    logger.info(f'''<{message.from_user.username}>: {message.text}''')


# Use ChatGPT for responses
@bot.message_handler(func=lambda msg: True)
def chat_gpt_complete(message):
    bot.reply_to(message, oif.get_response(message.text))
    logger.info(f'''<{message.from_user.username}>: {message.text}''')


bot.infinity_polling()
