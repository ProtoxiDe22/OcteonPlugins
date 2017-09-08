import core
import os
import json
PLUGINVERSION = 2
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = core.Plugin()
@plugin.command(command="/language",
                description="Changes bot language",
                inline_supported=True,
                hidden=False)
def locale_change(bot, update, user, args):
    with open(os.path.normpath("locale/locales.json")) as f:
        locale_list = json.load(f).keys()
    if len(args) > 0:
        if args[0] in locale_list:
            with open(os.path.normpath("plugdata/chat_locales.json")) as f:
                user_locales = json.load(f)
            with open(os.path.normpath("plugdata/chat_locales.json"), 'w') as f:
                user_locales[str(update.message.chat.id)] = args[0]
                json.dump(user_locales, f)
            return core.message("Your language now is <code>%s</code>" % args[0], parse_mode="HTML")
        else:
            return core.message(text="Unknown language: <code>%s</code>" % args[0], parse_mode='HTML')
    else:
        return core.message(text="Locales:\n" + "\n".join(locale_list) + "\nUse <code>/language codename</code> to change language", parse_mode="HTML")
