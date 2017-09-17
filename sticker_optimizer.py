import core
from PIL import Image
from io import BytesIO
import logging
LOGGER = logging.getLogger("Sticker Optimizer")
PLUGINVERSION = 2
size = (512, 512)
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = core.Plugin()
@plugin.command(command="/sticker_optimize",
                description="Optimizes image/file for telegram sticker",
                inline_supported=False,
                hidden=False)
def sopt(bot, update, user, args):
    io = BytesIO()
    if update.message.photo:
        fl = update.message.photo[-1]
    elif update.message.document:
        fl = update.message.document
    else:
        return core.message("You didnt supply picture as file/document")
    # LOGGER.debug(fl)
    fl = bot.getFile(fl.file_id)
    fl.download(out=io)
    io.seek(0)
    image = Image.open(io)
    image.thumbnail(size, Image.ANTIALIAS)
    io_out = BytesIO()
    quality = 80
    image.save(io_out, "PNG", quality=quality)
    while 1:
        quality -= 10
        io_out = BytesIO()
        image.save(io_out, "PNG", quality=quality)
        io_out.seek(0)
        if io_out.tell() < 358400:
            break
    return core.message(file=io_out)

