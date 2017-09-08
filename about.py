from settings import ABOUT_TEXT
import subprocess
import platform
import telegram
import core
PLUGINVERSION = 2
plugin = core.Plugin()
ABOUT_STRING = "Octeon-PTB based on commit <code>" + subprocess.check_output('git log -n 1 --pretty="%h"', shell=True).decode('utf-8') + "</code>"
ABOUT_STRING += subprocess.check_output('git --git-dir core/.git log -n 1 --pretty=" Octeon-Core based on commit <code>%h</code>"', shell=True).decode('utf-8')[1:]
ABOUT_STRING += subprocess.check_output('git --git-dir plugins/.git log -n 1 --pretty=" Octeon-Plugins based on commit <code>%h</code>"', shell=True).decode('utf-8')[1:]
ABOUT_STRING += "Python-Telegram-Bot version: <code>" + telegram.__version__ + "</code>\n"
ABOUT_STRING += "Running on <code>" + platform.platform() + "</code>." + "\nPython: <code>" + platform.python_implementation() + " " + platform.python_version() + "</code>\n"
ABOUT_STRING += '<a href="github.com/octonezd/core">GitHub page</a>\n'
ABOUT_STRING += ABOUT_TEXT
@plugin.command(command="/about",
                description="About bot",
                inline_supported=True,
                hidden=False)
def about(bot, update, user, args):
    return core.message(text=ABOUT_STRING, parse_mode="HTML")
