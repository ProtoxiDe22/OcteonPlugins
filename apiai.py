import core
import logging
import apiai
import settings
import json
import random
LOGGER = logging.getLogger("api.ai")
PLUGINVERSION = 2
assert settings.API_AI_TOKEN != ""
ai = apiai.ApiAI(settings.API_AI_TOKEN)
def handle_ai(bot, update):
    LOGGER.debug(update)
    req = ai.text_request()
    req.session_id = random.randint(0, 9999999999)
    req.query = update.message.text
    resp = json.loads(req.getresponse().read().decode("utf-8"))
    if not resp["result"]["action"].startswith("octobot"):
        return core.message(text=resp["result"]["fulfillment"]["speech"])
    else:
        ai_resp = bot.modloader.handle_ai(update, resp["result"]["action"])
        print("!!!!" + ai_resp)
        if ai_resp:
            ai_resp = ai_resp(bot, update, resp)
            ai_resp.reply_to_prev_message = False
            LOGGER.debug(ai_resp.reply_to_prev_message)
            return ai_resp
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = core.Plugin()
@plugin.message(regex=".*")
def apiai_provider(bot, update):
    LOGGER.debug("Hello World")
    airesp = None
    react = settings.AI_REACT
    react.append(bot.getMe().first_name)
    for pseudoname in react:
        if pseudoname.lower() in update.message.text.lower():
            airesp = handle_ai(bot, update)
    if update.message.reply_to_message:
        if update.message.reply_to_message.from_user == bot.getMe():
            airesp = handle_ai(bot, update)
    if airesp:
        airesp.reply_to_prev_message = False
    return airesp
