import logging
import csv
from io import StringIO

import requests

import core

PLUGINVERSION = 2
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = core.Plugin()
CURR_TEMPLATE = """
%(in)s = %(out)s

%(date)s
Data from Yahoo Finance
"""
LOGGER = logging.getLogger("/cash")

def convert(in_c, out_c, count):
    rate = requests.get(
        "http://download.finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1",
        params={
            "s": in_c + out_c + "=X"
        }
    )
    LOGGER.debug(rate.text)
    csv_rate = list(csv.reader(StringIO(rate.text), delimiter=","))[0]
    if csv_rate[1] == "N/A":
        raise NameError("Invalid currency")
    else:
        out = {}
        out["in"] = "%s %s" % (count, in_c.upper())
        out["out"] = "%s %s" % (round(float(count)*float(csv_rate[1]), 2), out_c.upper())
        out["date"] = csv_rate[-2] + " " + csv_rate[-1]
        return out

@plugin.command(command="/cash",
                description="Converts currency",
                inline_supported=True,
                required_args=3,
                hidden=False)
def currency(bot, update, user, args):
    """
    Powered by Yahoo Finance
    Example usage:

    User:
    /cash 100 RUB USD

    OctoBot:
    100 RUB = 1.66 USD

    8/7/2017 10:30pm
    Data from Yahoo Finance
    """
    if len(args) < 3:
        return core.message(text="Not enough arguments! Example:<code>/cash 100 RUB USD</code>",
                              parse_mode="HTML",
                              failed=True)
    else:
        try:
            rate = convert(args[1], args[-1], args[0])
        except NameError:
            return core.message('Bad currency name', failed=True)
        else:
            return core.message(CURR_TEMPLATE % rate)

@plugin.ai("octobot.cash")
def ai_cash(bot, update, aidata):
    out_c = aidata["result"]["parameters"]["currency-name"]
    in_c = aidata["result"]["parameters"]["unit-currency"]["currency"]
    count = aidata["result"]["parameters"]["unit-currency"]["amount"]
    try:
        rate = convert(in_c, out_c, count)
    except NameError:
        return core.message("Aw, I dont think Yahoo Finance knows that currency :(")
    else:
        return core.message(text=aidata["result"]["fulfillment"]["speech"] % rate)
