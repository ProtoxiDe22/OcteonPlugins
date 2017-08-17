"""
Word swap module
"""
import logging, time, json

from telegram import Bot, Update
from telegram.ext import Filters, MessageHandler, Updater

import constants # pylint: disable=E0401


def preload(updater: Updater, level):
    """
    This loads whenever plugin starts
    Even if you dont need it, you SHOULD put at least
    return None, otherwise your plugin wont load
    """
    return
def diario(bot: Bot, update: Update, user, args):
    msg = update.message
    txt = msg.text
    logging.debug(msg)
    if msg.reply_to_message is not None:
        txt = msg.reply_to_message.text
        user = msg.reply_to_message.from_user.name
    else:
        txt = txt.lstrip('/diario')
        user = msg.from_user.name
    txt = txt.strip();
    if not txt:
        return None, constants.NOTHING
    serializedData = json.dumps({'sender': user, 'text' : txt, 'timestamp':time.time()})
    file = open("./diario.json","r+b")
    file.seek(-1,2)
    file.write(bytearray(','+serializedData+']', 'utf8'))
    file.close()
    msg.reply_text("aggiunto al diario!")
    return None

COMMANDS = [
    {
        "command":"/diario",
        "function":diario,
        "description":"Adds a diary entry!",
        "inline_support": False
    }
]
