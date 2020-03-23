#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import logging
import datetime
import requests

from setup import PROXY, TOKEN
from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


log=[]
def log_f(func):
    def inner(*args, **kwargs):
        """For showing time"""
        now = datetime.datetime.now()
        func(*args,**kwargs)
        info = dict()
        info["username"]=args[0].effective_user.first_name
        try:
            info["username"]+= " " + args[0].effective_user.last_name
        except BaseException:
            pass
        info["nickname"]=args[0].effective_user.username
        info["funcname"]=func.__name__
        info["message"]=args[0].message.text
        info["date"]=str(now)
        global log
        log.append(info)
        with open("bot_log.txt", "a", encoding="utf-8") as log_open:
            for i in range(len(log)):
                print(log[i], file=log_open)
    return inner

@log_f
def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Привет, {update.effective_user.first_name}!')


@log_f
def chat_help(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Введи команду /start для начала. ')

@log_f
def echo(update: Update, context: CallbackContext):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

@log_f
def chat_history(update: Update, context: CallbackContext):
    """Echo the user history."""
    """message is the answer for a user"""
    message=''
    """File with the name of user"""
    with open(f"log_{update.effective_user.first_name}.txt","a", encoding="utf-8") as fopen:
        counter=0

        """searching last 5 or less messages for this user, logging to the file and forming the answer"""
        for i in range(len(log)):
            if (log[len(log)-1-i]['nickname'] == update.effective_user.username):
                print(log[len(log)-1-i],file=fopen)
                message=log[len(log)-1-i]["message"] + "\n" + message
                counter += 1
            if counter == 5:
                break

        update.message.reply_text(f"History:\n{message}")

@log_f
def fact(update: Update, context: CallbackContext):
    r = requests.get('https://cat-fact.herokuapp.com/facts')
    d = r.json()
    maxv = 0
    if r.status_code == 200:
        for i in range(len(d['all'])):
            if d['all'][i]['upvotes'] >= maxv:
                maxv = d['all'][i]['upvotes']
                fact = d['all'][i]['text']
        update.message.reply_text(f"Fact: \n{fact}")
    else:
        update.message.reply_text(f"Error: \n{r.status_code}")

@log_f
def weather(update: Update, context: CallbackContext):
    message=''
    r = requests.get(
        'https://yandex.ru/pogoda/47?utm_source=serp&utm_campaign=wizard&utm_medium=desktop&utm_content=wizard_desktop_main&utm_term=title')
    d = r.text

    position = d.rfind(
        '<div class="temp fact__temp fact__temp_size_s" role="text"><span class="temp__pre-a11y a11y-hidden">Текущая температура</span><span class="temp__value">') + len(
        '<div class="temp fact__temp fact__temp_size_s" role="text"><span class="temp__pre-a11y a11y-hidden">Текущая температура</span><span class="temp__value">')
    temperature = ''
    i = 0
    while d[position + i] != "<":
        temperature += d[position + i]
        i += 1
    position = d.find('<div class="link__condition day-anchor i-bem" data-bem=') + len(
        '<div class="link__condition day-anchor i-bem" data-bem=')
    fl = False
    condition = ''
    i = 0
    while d[position + i] != "<":
        if fl:
            condition += d[position + i]
        if d[position + i] == ">":
            fl = True
        i += 1
    message +='Температура: ' + temperature + "\n" + condition
    update.message.reply_text(message)


@log_f
def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')


def main():
    bot = Bot(
        token=TOKEN,
        base_url=PROXY,  # delete it if connection via VPN
    )
    updater = Updater(bot=bot, use_context=True)

    # on different commands - answer in Telegram
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', chat_help))
    updater.dispatcher.add_handler(CommandHandler('history', chat_history))
    updater.dispatcher.add_handler(CommandHandler('fact', fact))
    updater.dispatcher.add_handler(CommandHandler('weather', weather))

    # on noncommand i.e message - echo the message on Telegram
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    logger.info('Start Bot')
    main()
