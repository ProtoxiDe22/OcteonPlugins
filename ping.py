import octeon
PLUGINVERSION = 2
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = octeon.Plugin()
@plugin.command(command="/ping",
                description="Command for checking if bot is alive",
                inline_supported=True,
                hidden=False)
def hi(bot, update, user, args):
    return octeon.message(text="Pong!")
