#!/usr/bin/env python3

import covid
import logging
import sys
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# handling arguments
def list(update, context):
    number = context.args[0]
    if not number.isdigit():
        error(update, context, True)
    else:
        update.message.reply_text("shows list of top {0} countries! ".format(context.args[0]))


def error(update, context, iserror=False):
    """Send a message when unknown message is issued or when wrong data """
    message = "Usages:\n\
/get <country> - gets data on specified country\n\
/list <number> - gets specified top infected countries\n\
/news <topic> - gets results on topic regarding covid"

    if iserror:
        message = "`Invalid argument input!\n" + message + "`"
    else:
        message = "`Invalid argument!\n" + message + "`"
    update.message.reply_text(message, parse_mode="Markdown")


def get(update, context):
    country = context.args[0]
    message = "`" + covid.getcountry(country) + "`"
    pythoupdate.message.reply_text(message, parse_mode="Markdown")


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(sys.argv[1])

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("list", list))
    dispatcher.add_handler(CommandHandler("get", get))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, error))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
