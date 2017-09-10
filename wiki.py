from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
from requests import get
import html
import core
import re
import logging


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

apiurl = "https://en.wikipedia.org/w/api.php"
message = """
<b>%(title)s</b>

<i>%(extract)s</i>

<a href="en.wikipedia.org/wiki/%(title)s">Article on Wikipedia</a>
"""
PLUGINVERSION = 2
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = core.Plugin()
HEADERS = {"User-Agent": "OctoBot/1.0"}
LOGGER = logging.getLogger("Wiki")


def get_definition(term, number):
    definition = get(apiurl,
                     params={
                         "action": "query",
                         "format": "json",
                         "list": "search",
                         "srsearch": term,
                         "srinfo": "totalhits",
                         "srprop": ""
                     },
                     headers=HEADERS).json()
    if definition["query"]["search"]:
        defpath = definition["query"]["search"][number-1]
        deftxt = list(get(apiurl, params={
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "list": "",
            "pageids": defpath["pageid"],
            "explaintext": 1,
            "exsentences": 4
        }).json()["query"]["pages"].values())[0]
        deftxt = escape_definition(deftxt)
        LOGGER.debug(defpath)
        LOGGER.debug(deftxt)
        return message % deftxt, definition["query"]["searchinfo"]["totalhits"]
    else:
        raise IndexError("Not found")


def escape_definition(definition):
    for key, value in definition.items():
        if isinstance(value, str):
            definition[key] = html.escape(cleanhtml(value))
    return definition


@plugin.command(command="/wiki",
                description="Searches for query in wikipedia",
                inline_supported=True,
                required_args=1,
                hidden=False)
def wikipedia(_: Bot, ___: Update, user, args):
    defnum = 1
    term = " ".join(args)
    try:
        definition = get_definition(term, defnum)
    except IndexError:
        return core.message("Nothing found!", failed=True)
    else:
        kbd = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="⬅️", callback_data="wiki:bwd:" +
                                     str(defnum) + ":" + term + ":" + str(definition[1])),
                InlineKeyboardButton(
                    text="1/" + str(definition[1]), callback_data="none"),
                InlineKeyboardButton(text="➡️", callback_data="wiki:fwd:" +
                                     str(defnum) + ":" + term + ":" + str(definition[1]))
            ]
        ])
        return core.message(definition[0], parse_mode="HTML", inline_keyboard=kbd)


@plugin.inline_button("wiki")
def wikipedia_pswitch(bot, update, query):
    data = query.data.split(":")
    term = data[3]
    defnum = None
    if data[1] == "fwd":
        if not int(data[2]) + 1 > int(data[-1]):
            defnum = int(data[2])+1
    elif data[1] == "bwd":
        if not int(data[2]) - 1 <= 0:
            defnum = int(data[2]) - 1
    if (not data[2] == defnum) and defnum:
        definition = get_definition(term, defnum)
        update.effective_message.edit_text(definition[0], parse_mode="HTML")
        kbd = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="⬅️", callback_data="wiki:bwd:" +
                                     str(defnum) + ":" + term + ":" + str(definition[1])),
                InlineKeyboardButton(
                    text=str(defnum) + "/" + str(definition[1]), callback_data="none"),
                InlineKeyboardButton(text="➡️", callback_data="wiki:fwd:" +
                                     str(defnum) + ":" + term + ":" + str(definition[1]))
            ]
        ])
        update.effective_message.edit_reply_markup(reply_markup=kbd)
