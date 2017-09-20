import core
import apiai
import settings
import json
import random
PLUGINVERSION = 2
assert settings.API_AI_TOKEN != ""
ai = apiai.ApiAI(settings.API_AI_TOKEN)
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = core.Plugin()
@plugin.message(regex=".*")
def apiai_provider(bot, update):
    react = settings.AI_REACT
    react.append(bot.getMe().first_name)
    for pseudoname in react:
        if pseudoname.lower() in update.message.text.lower():
            req = ai.text_request()
            req.session_id = random.randint(0, 9999999999)
            req.query = update.message.text
            resp = json.loads(req.getresponse().read().decode("utf-8"))
            if not resp["result"]["action"].startswith("octobot"):
                return core.message(text=resp["result"]["fulfillment"]["speech"])
            else:
                ai_resp = bot.modloader.handle_ai(update, resp["result"]["action"])
                if ai_resp:
                    return ai_resp(bot, update, resp)