"""
Echo plugin example
"""
import core
import pprint
import logging
PLUGINVERSION = 2
LOGGER = logging.getLogger("AntiSpamBot")
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
SPAMBOTS_RAW = """
@pollsce
@acing
@GroupManagerDomina
@GroupManagerDomina
@akeredbot
@pedoannihilation
@RcSmerdbot
@RCBAD_BOT
@PedoAnnihilation
@lipped_bot
@sbfdskvgld_bot
@akered
@floodmeh
@opsmerderdated
@DrogaPazza_bot
@herhhhhhhhhhhhhhhhhhhbot
@opsmserdedetgbot
@ilcristoBot
@opskekekekbot
@opsksksksk_bot
@BaudaStorm
@ssflood
@nasakedbot
@SsFlood
@AKED_BY_GANJIA
@Shitstorm
@AkedByGanjia
@SonounbravoebelloBot
@sorrowful
@sorrowful10bot
@Floodmeh
@otifaciao
@Mallibot
@uhdhuahs7dys7uhadsubot
@d17shdnam1j1kbot
@bd817udhausdhuhbot
@sorrowful
@xxxPLxxx_bot
@Missafricabot
@hscbot
@Vip835bot
@Hilal99bot
@Ripgroup
@d17shdnam1j1kbot
@dj1771ah1jaka1obot
@bd817udhausdhuhbot
@dag71suhaj1y7a1jbot
@mother
@githubchatbot
@eucodesmerdbot
@blunterblackbot
@TumblrItaliaBot
@NoEscape_bot
@DominioPubblicoBot
@TumblrITbot
@YoungAndreaBot
@AkedBaiAL
@CarabiniereDomina
@SiOkCiao
@Cowboys
""".strip("\n")
SPAMBOTS = []
for sbot in SPAMBOTS_RAW.split("\n"):
    sbot = sbot.lower()
    if sbot.startswith("@"):
        SPAMBOTS.append(sbot[1:])
    else:
        SPAMBOTS.append(sbot)
SPAMBOTS = set(SPAMBOTS)
LOGGER.debug(SPAMBOTS)
plugin = core.Plugin()
@plugin.update()
def antispambot(bot, update):
    if update.message:
        if update.message.new_chat_members:
            for new_user in update.message.new_chat_members:
                if new_user.is_bot:
                    for spambot in SPAMBOTS:
                        if new_user.username.lower().startswith(spambot):
                            for admin in update.message.chat.get_administrators():
                                print(admin.user.id)
                                print(bot.get_me().id)
                                if admin.user.id == bot.get_me().id:
                                    bot.kickChatMember(update.message.chat.id, new_user.id)
                                    return core.message("%s was kicked due to being in spam blacklist" % new_user.first_name)
                            return core.message("Warning! This bot is in my blacklist for spam, I would be happy to ban it, but I am not admin here.")
    # print("HEY B0SS")
    # return core.message(text=pprint.pformat(update))

