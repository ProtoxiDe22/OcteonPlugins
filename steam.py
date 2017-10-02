"""Steam module"""
import core
from telegram import Bot, Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from requests import get
import xmltodict
import constants


def getuser(url):
    r = xmltodict.parse(
        get("http://steamcommunity.com/id/%s/?xml=1" % url).text)
    return dict(r)


PLUGINVERSION = 2
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = core.Plugin()


@plugin.command(command="/steam",
                description="Sends info about profile on steam. Use custom user link. Example:/steam gabelogannewell",
                inline_supported=True,
                hidden=False)
def steam(b: Bot, u: Update, user, args):
    """
    Example usage:
    User A: Where is pyro update?
    User B: Ask him
    User B: /steam gabelogannewell
    Bot: [Account userpic]
    Bot:
    User:Rabscuttle
    SteamID64:76561197960287930
    Last Online
    🛡️User is not VACed
    💱User is not trade banned
    🔓User account is not limited
    ⚠️User account visibility is limited
    """
    if len(args) >= 1:
        account = getuser(args[0])
        if "response" in account:
            return "Cant find this user!", constants.TEXT, "failed"
        else:
            message = ""
            user = account["profile"]
            message += "User:%s\n" % user["steamID"]
            message += "SteamID64:%s\n" % user["steamID64"]
            message += "%s\n" % user["stateMessage"]
            message += "🛡️"
            if user["vacBanned"] == '0':
                message += "User is not VACed\n"
            else:
                message += "User is VACed\n"
            message += "💱"
            if user["tradeBanState"] == "None":
                message += "User is not trade banned\n"
            else:
                message += "User is trade banned\n"
            if user["isLimitedAccount"] == '0':
                message += "🔓User account is not limited\n"
            else:
                message += "🔒User account is limited\n"
            if user["privacyState"] == "public":
                message += "User is member since %s\n" % user["memberSince"]
            else:
                message += "⚠️User account visibility is limited"
            keyboard = [
                [InlineKeyboardButton(
                    "➕Add to friends", url="http://core.octonezd.pw/steam.html?steamid=" + user["steamID64"])]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            return [user["avatarFull"], message, markup], constants.PHOTOWITHINLINEBTN
    else:
        return "Custom link is not supplied!", constants.TEXT, "failed"

COMMANDS = [
    {
        "command":"/steam",
        "function":steam,
        "description":"Sends info about profile on steam. Use custom user link. Example:/steam n3cat",
        "inline_support":True
    }
]
