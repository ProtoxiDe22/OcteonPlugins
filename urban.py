from telegram.ext import Updater, CommandHandler
from telegram import Bot, Update
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
@plugin.command(command="/ud",
                description="Searches for definition of specfied word in urban dictionary",
                inline_supported=True,
                hidden=False)
def urband(_: Bot, ___: Update, user, args):
    """/ud"""
    definition = get(apiurl, params={
        "term":" ".join(args)
    }).json()
    if definition["result_type"] == "exact":
        definition = definition["list"][0]
        msg = message % definition
        return octeon.message(msg, parse_mode="HTML")
    else:
        return octeon.message("Nothing found!", failed=True)

