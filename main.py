#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import time
import requests
import threading
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# For recording the audio
from collections import deque
q = deque( maxlen=514 )
recordings = {}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    bot.send_message(chat_id=update.message.chat_id, text='Use /clip to clip diodi')


def clip(bot, update):
    """Send a message when the command /help is issued."""
    start = time.time()
    sender = update.message.from_user
    sendertext = "{} {} @{}".format(sender.first_name, getattr(sender, 'last_name', ''), getattr(sender, 'username', ''))
    print("{} is recording from {}".format(sendertext, start))
    with open('diodi.mp3', 'wb') as f:
        for block in q:
            f.write(block)
    with open('diodi.mp3', 'rb') as f:
        bot.send_voice(update.message.chat_id, f, timeout=20)

def rec_start(bot, update):
    sender = update.message.from_user
    if sender.id in recordings:
        rec_end(bot, update, recordings[sender.id])
        del recordings[sender.id]
    else:
        sendertext = "{} {} @{}".format(sender.first_name, getattr(sender, 'last_name', ''), getattr(sender, 'username', ''))
        print("{} started to record".format(sendertext))
        recordings[sender.id] = deque( maxlen=1280 )


def rec_end(bot, update, record):
    sender = update.message.from_user
    sendertext = "{} {} @{}".format(sender.first_name, getattr(sender, 'last_name', ''), getattr(sender, 'username', ''))
    print("{} recorded {} blocks".format(sendertext, len(record)))
    with open('rec.mp3', 'wb') as f:
        for block in record:
            f.write(block)
    with open('rec.mp3', 'rb') as f:
        bot.send_voice(update.message.chat_id, f, timeout=20)
        

def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', bot, update.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("719806814:AAGYz51c18jP2nLRBobWx1gpq8KauLmGJio")
    # updater = Updater("890403817:AAEg-CKr7K06KE4YUg4YwfIh3PZw0w4-v_w")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("clip", clip))
    dp.add_handler(CommandHandler("rec", rec_start))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


def listen_to_diodi():
    stream_url = 'https://virta.radiodiodi.fi/mp3'
    r = requests.get(stream_url, stream=True)
    while(1):
        try:
            for block in r.iter_content(1024):
                q.append(block)
                for key in recordings:
                    recordings[key].append(block)
        except (KeyboardInterrupt, SystemExit):
            break
        except:
            pass



if __name__ == '__main__':
    threading.Thread(target=listen_to_diodi).start()
    main()
