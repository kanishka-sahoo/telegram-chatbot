#!/usr/bin/python3
import telebot
import os
from dotenv import load_dotenv
import openai_interface as oif
import requests
import json
from telegram.ext import *
import logging
import openai
load_dotenv()

# initialise bot
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
oif.invoke_key(os.environ.get('API_TOKEN'))

init_msg = """
You are a conversational AI Chatbot specialising in positive user interaction.
Pretend to be human wherever and whenever possible.

Respond to technical, complex questions to the best of your abilities
Refrain from calling a question complex, and try to solve it instead.
"""
user_init_text = """
Welcome to Tele-GPT! Here are a few useful commands.
/start : Brings up this message.
/clearchat : clears the chat history, on OpenAI's servers
/ping : Tests the server connection, replies with Pong!
/support : Log complaints directly to the server logs

Remember to stick to OpenAI's Content Policies and avoid misuse or spam.
If you find any errors, reach out by typing /support.
Also remember, all messages you send are logged for review.
You may be asked to stop using the service if you ask for
inappropriate requests
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
    if username == "None" or username == None or username == "none":
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
        bot.reply_to(
            message, 'Please add a username to your account for chat security.')
    else:
        ctx_user.messages = []
        bot.reply_to(message, 'Cleared Chat')
        logger.info(f'''<{message.from_user.username}>: {message.text}''')

# When user first starts a chat


@bot.message_handler(commands=['start'])
def initiate(message):
    ctx_user = do_user_action(str(message.from_user.username))
    if ctx_user == 0xDEADBEEF:
        bot.reply_to(
            message, 'Please add a username to your account for chat security.')
    else:
        bot.reply_to(message, user_init_text)
        logger.info(f'''<{message.from_user.username}>: {message.text}''')


@bot.message_handler(commands=['support'])
def support(message):
    ctx_user = do_user_action(str(message.from_user.username))
    if ctx_user == 0xDEADBEEF:
        bot.reply_to(
            message, 'Please add a username to your account for chat security.')
    else:
        bot.reply_to(message, 'Your message has been logged')
        logger.info(f'''<{message.from_user.username}>: {message.text}''')


# Use ChatGPT for responses
@bot.message_handler(func=lambda msg: True)
def chat_gpt_complete(message):
    ctx_user = do_user_action(str(message.from_user.username))
    if ctx_user == 0xDEADBEEF:
        bot.reply_to(
            messsage, 'Please add a username to your account for chat security.')
    else:
        try:
            bot.reply_to(message, ctx_user.get_response(message.text))
            logger.info(f'''<{message.from_user.username}>: {message.text}''')
        except openai.error.InvalidRequestError:
            bot.reply_to(
                message, "You have run out of OpenAI messages, please run /clearchat to continue")


bot.infinity_polling()
