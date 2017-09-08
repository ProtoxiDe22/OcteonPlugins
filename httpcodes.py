# -*- coding: utf-8 -*-
"""
http status codes
"""
import logging

from telegram import Bot, Update
import requests
import core

LOGGER = logging.getLogger("HTTP codes")
CODES = requests.get(
    "https://github.com/for-GET/know-your-http-well/raw/master/json/status-codes.json").json()
MESSAGE = """
%(code)s - %(phrase)s
%(spec_title)s
%(description)s
Link to specification:%(spec_href)s
"""

PLUGINVERSION = 2
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = core.Plugin()


@plugin.command(command="/httpcode",
                description="Sends information about specific http status code",
                inline_supported=True,
                required_args=1,
                hidden=False)
def get_code(_: Bot, __: Update, ___, args):  # pylint: disable=W0613
    """
    Example usage:
    User: /httpcode 451
    Bot:451 - Unavailable For Legal Reasons
    draft-ietf-httpbis-legally-restricted-status
    "This status code indicates that the server is denying access to the resource in response to a legal demand."
    Link to specification:https://tools.ietf.org/html/draft-ietf-httpbis-legally-restricted-status
    """

    if len(args[0]) == 3:
        for code in CODES:
            if args[0] == code["code"]:
                return core.message(MESSAGE % code)
        return core.message("Cant find " + args[0], failed=True)
    else:
        return core.message("Invalid code passed:" + args[0], failed=True)
