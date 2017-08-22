"""
Yandex Translation API
"""
import logging
from urllib.parse import quote

from telegram import Bot, Update
from telegram.ext import Updater
from requests import post

import constants # pylint: disable=E0401
import settings
import octeon

LOGGER = logging.getLogger("YTranslate")
YAURL = "https://translate.yandex.net/api/v1.5/tr.json/translate?"
YAURL += "key=%s" % settings.YANDEX_TRANSLATION_TOKEN

def preload(updater: Updater, level):
    """
    This loads whenever plugin starts
    Even if you dont need it, you SHOULD put at least
    return None, otherwise your plugin wont load
    """
    return

def translate(bot: Bot, update: Update, user, args): # pylint: disable=W0613
    """/tl"""
    if update.message.reply_to_message:
        if len(args) > 0:
            lang = args[0].lower()
        else:
            lang = "en"
        yandex = post(YAURL, params={"text":update.message.reply_to_message.text, "lang":lang}).json()
        if "lang" in yandex:
            return octeon.message(yandex["lang"].upper() + "\n" + yandex["text"][0] + "\n\nPowered by Yandex Translate API")
        else:
            return octeon.message(yandex["message"], failed=True)

COMMANDS = [
    {
        "command":"/tl",
        "function":translate,
        "description":"Translates message to english. Example: [In Reply To Message] /tl",
        "inline_support":True
    }
]
