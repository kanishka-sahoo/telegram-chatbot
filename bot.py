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
oif.invoke_key(os.environ.get('API_TOKEN'))

init_msg = """
You are a conversational AI Chatbot specialising in positive user interaction. Pretend to be human wherever and whenever possible.

1) If you are faced with a question you cannot or are not allowed to answer, reply as a human would.
2) If asked about events outside your knowledge cutoff, or about recent events, just say that you don't know. 
3) If the content asked violates OpenAI policy, just simply decline to answer the question, as a human. 
4) Try not to mention that you are AI or a language model.
5) When asked for the following, reply as shown or similar:
    user asks for the (date/time) -> the (date/time) is ${(date/time)}
    user asks for the weather in given city -> the weather in given city is ${weather[city]}
    user asks for other current info -> I don't have the current info.
"""


# setting up logging
logging.basicConfig(filename="messages.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

total_users_chats = []

# handle the bot request pipeline
def do_user_action(username):
    if username == "None" or username == None:
        return 0xDEADBEEF
    for i in total_users_chats:
        if i and i.username == username:
            return i
    else:
        new_user = oif.OpenAIBot(init_msg, username)
        total_users_chats.append(new_user)
        return new_user


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
    ctx_user = do_user_action(str(message.from_user.username))
    if ctx_user == 0xDEADBEEF:
        bot.reply_to(message, 'Please add a username to your account for chat security.')
    else:
        ctx_user.messages = []
        bot.reply_to(message, 'Cleared Chat')
        logger.info(f'''<{message.from_user.username}>: {message.text}''')


# Use ChatGPT for responses
@bot.message_handler(func=lambda msg: True)
def chat_gpt_complete(message):
    ctx_user = do_user_action(str(message.from_user.username))
    if ctx_user == 0xDEADBEEF:
        bot.reply_to(messsage, 'Please add a username to your account for chat security.')
    else:
        bot.reply_to(message, ctx_user.get_response(message.text))
        logger.info(f'''<{message.from_user.username}>: {message.text}''')


bot.infinity_polling()
