"""Timezones"""
from telegram import Bot, Update
import pendulum
import octeon

from pytzdata.exceptions import TimezoneNotFound
TIMEFORMAT = '%A %d%tof %B %Y %H:%M:%S'

PLUGINVERSION = 2
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = octeon.Plugin()


@plugin.command(command="/tz",
                description="Sends info about specifed zone(for example:Europe/Moscow)",
                inline_supported=True,
                required_args=1,
                hidden=False)
def timezonecmd(_: Bot, update: Update, user, args):
    """
    Example usage:
    User: /tz Europe/Moscow
    Bot: Europe/Moscow: Friday 18 of August 2017 08:21:04
    """
    timezone = " ".join(args)
    try:
        timezone = pendulum.now(timezone)
    except TimezoneNotFound:
        return octeon.message("⚠You specifed unknown timezone", failed=True)
    else:
        return octeon.message(timezone.timezone_name + ": " + timezone.format(TIMEFORMAT))
