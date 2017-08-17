import octeon
import markovify as markov
PLUGINVERSION = 2
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = octeon.Plugin()

file = open('./markovModel.json')
model = markov.NewlineText.from_json(file.read())
file.close()
tempmodel, saveindex = '', 0

@plugin.message(regex=".*") # You pass regex pattern
def generate_chain(bot, update):
    global model
    global saveindex
    if(update.message.text.startswith('/')):
        return None
    tempmodel = markov.NewlineText(update.message.text)
    model = markov.combine([model, tempmodel])
    saveindex += 1
    if saveindex >= 9:
        save()
    return None
@plugin.command(command="/markov",
                description="generates a message with markov chains",
                inline_supported=False,
                hidden=False)
def generate_message(bot, update, user, args):
    generatedmessage = model.make_sentence(tries = 50)
    if generatedmessage == None:
        return octeon.message(text="message generation failed")
    return octeon.message(text = generatedmessage)
    
def save():
    global saveindex
    saveindex = 0
    json = model.to_json()
    file = open('./markovModel.json','w')
    file.write(json)
    file.close()
    return None
