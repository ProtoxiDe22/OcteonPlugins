"""
Word swap module
"""
import re
import logging

from telegram import Bot, Update
from telegram.ext import Filters, MessageHandler, Updater

import octeon
PLUGINVERSION = 2
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = octeon.Plugin()
@plugin.command(command="/s/",
                description="Swaps word in message",
                inline_supported=True,
                hidden=False)
def wordsw(bot: Bot, update: Update, user, args):
    """
    Example usage:
    User A
    Hi

    User B
    [In reply to User A]
    /s/Hi/Bye

    Octeon
    Hello, User A
    Did you mean:
    Bye
    """
    msg = update.message
    txt = msg.text
    logging.debug(msg)
    if msg.reply_to_message is not None:
        if txt.startswith("/s"):
            if not msg.reply_to_message.from_user.name == bot.getMe().name:
                origword = txt[2]
                swap = txt[3]
                groups = [b.replace("\/", "/") for b in re.split(r"(?<!\\)/", txt)]
                find = groups[2]
                replacement = groups[3]
                if len(groups) > 4:
                    flags = groups[4]
                else:
                    flags = ""
                if len(origword) > 0:
                    find_re = re.compile("{}{}".format("(?{})".format(flags.replace("g", "")) if flags.replace("g", "") != "" else "", find))
                    mod_msg = find_re.sub("<b>" + replacement + "</b>", msg.reply_to_message.text, count=int("g" not in flags))
                    text = "Hello, {}\nDid you mean:\n{}".format(
                            msg.reply_to_message.from_user.first_name,
                            mod_msg
                    )
                    return octeon.message(text=text, parse_mode="HTML")
