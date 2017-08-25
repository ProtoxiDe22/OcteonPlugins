import logging
import csv
from io import StringIO

import requests

import octeon

PLUGINVERSION = 2
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = octeon.Plugin()
CURR_TEMPLATE = """
%s %s = %s %s

%s %s
Data from Yahoo Finance
"""
LOGGER = logging.getLogger("/cash")


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

    Octeon:
    100 RUB = 1.66 USD

    8/7/2017 10:30pm
    Data from Yahoo Finance
    """
    if len(args) < 3:
        return octeon.message(text="Not enough arguments! Example:<code>/cash 100 RUB USD</code>",
                              parse_mode="HTML",
                              failed=True)
    else:
        rate = requests.get(
            "http://download.finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1",
            params={
                "s": args[1] + args[-1] + "=X"
            }
        )
        LOGGER.debug(rate.text)
        csv_rate = list(csv.reader(StringIO(rate.text), delimiter=","))[0]
        if csv_rate[1] == "N/A":
            return octeon.message('Bad currency name', failed=True)
        else:
            return octeon.message(CURR_TEMPLATE % (
                args[0],
                args[1],
                round(float(args[0])*float(csv_rate[1]), 2),
                args[-1],
                csv_rate[-2],
                csv_rate[-1]
            ))
