from settings import ABOUT_TEXT
import subprocess
import platform
import telegram
import octeon
PLUGINVERSION = 2
plugin = octeon.Plugin()
ABOUT_STRING = "Octeon-PTB based on commit <code>" + subprocess.check_output('git log -n 1 --pretty="%h"', shell=True).decode('utf-8') + "</code>"
ABOUT_STRING += "Octeon-Core based on commit <code>" + subprocess.check_output('git log -n 1 --pretty="%h" -C octeon', shell=True).decode('utf-8') + "</code>"
ABOUT_STRING += "Octeon-Plugins based on commit <code>" + subprocess.check_output('git log -n 1 --pretty="%h" -C plugins', shell=True).decode('utf-8') + "</code>"
ABOUT_STRING += "Python-Telegram-Bot version: <code>" + telegram.__version__ + "</code>\n"
ABOUT_STRING += "Running on <code>" + platform.platform() + "</code>." + "\nPython: <code>" + platform.python_implementation() + " " + platform.python_version() + "</code>\n"
ABOUT_STRING += ABOUT_TEXT
@plugin.command(command="/about",
                description="About bot",
                inline_supported=True,
                hidden=False)
def about(bot, update, user, args):
    return octeon.message(text=ABOUT_STRING, parse_mode="HTML")
