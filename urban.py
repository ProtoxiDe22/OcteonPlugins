from telegram.ext import Updater, CommandHandler
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
from requests import get
from html import escape
import octeon
apiurl = "http://api.urbandictionary.com/v0/define"
message = """
Definition for <b>%(word)s</b> by %(author)s:
%(definition)s

Examples:
<i>
%(example)s
</i>
<a href="%(permalink)s">Link to definition on Urban dictionary</a>
"""
PLUGINVERSION = 2
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = octeon.Plugin()
def get_definition(term, number):
    definition = get(apiurl, params={
        "term":term
    }).json()
    if definition["result_type"] == "exact":
        deftxt = definition["list"][int(number)-1]
        return message % deftxt, len(definition["list"])
    else:
        raise IndexError("Not found")

@plugin.command(command="/ud",
                description="Searches for definition of specfied word in urban dictionary",
                inline_supported=True,
                hidden=False)
def urband(_: Bot, ___: Update, user, args):
    """/ud"""
    defnum = 1
    term = " ".join(args)
    try:
        definition = get_definition(term, defnum)
    except IndexError:
        return octeon.message("Nothing found!", failed=True)
    else:
        kbd = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="⬅️", callback_data="ud:bwd:" + str(defnum) + ":" + term + ":" + str(definition[1])),
                InlineKeyboardButton(text="1/" + str(definition[1]), callback_data="none"),
                InlineKeyboardButton(text="➡️", callback_data="ud:fwd:" + str(defnum) + ":" + term + ":" + str(definition[1]))
            ]
        ])
        return octeon.message(definition[0], parse_mode="HTML", inline_keyboard=kbd)

@plugin.inline_button("ud")
def urban_pswitch(bot, update, query):
    data = query.data.split(":")
    term = data[3]
    defnum = None
    if data[1] == "fwd":
        if not int(data[2])+1 > int(data[-1]):
            defnum = int(data[2])+1
    elif data[1] == "bwd":
        if not int(data[2])-1 <= 0:
            defnum = int(data[2])-1
    if (not data[2] == defnum) and defnum:
        definition = get_definition(term,defnum)
        update.effective_message.edit_text(definition[0], parse_mode="HTML")
        kbd = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="⬅️", callback_data="ud:bwd:" + str(defnum) + ":" + term + ":" + str(definition[1])),
                InlineKeyboardButton(text=str(defnum) + "/" + str(definition[1]), callback_data="none"),
                InlineKeyboardButton(text="➡️", callback_data="ud:fwd:" + str(defnum) + ":" + term + ":" + str(definition[1]))
            ]
        ])
        update.effective_message.edit_reply_markup(reply_markup=kbd)