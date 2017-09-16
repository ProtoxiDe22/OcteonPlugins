import core
import random
PLUGINVERSION = 2
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = core.Plugin()
@plugin.command(command="/first_message",
                description="Replies to first message in chat",
                inline_supported=False,
                hidden=False)
def fmsg(bot, update, user, args):
    bot.sendMessage(update.message.chat.id, "Here is first message in this chat", reply_to_message_id=1)

# @plugin.command(command="/random_message",
#                 description="Replies to random message in chat",
#                 inline_supported=False,
#                 hidden=False)
# def rmsg(bot, update, user, args):
#     bot.sendMessage(update.message.chat.id, "Random message", reply_to_message_id=random.randint(1, update.message.message_id))
