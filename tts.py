import core
from gtts import gTTS
from io import BytesIO
PLUGINVERSION = 2
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = core.Plugin()
@plugin.command(command="/tts",
                description="Text-To-Speech. You can supply language code as first argument",
                inline_supported=True,
                hidden=False,
                required_args=1)
def tts(bot, update, user, args):
    kw = {}
    if len(args[0]) == "2":
        kw["lang"] = args[0]
        kw["text"] = " ".join(args[1:])
    else:
        kw["text"] = " ".join(args)
    tts = gTTS(**kw)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return core.message(voice=fp)
