import core as octeon, requests, constants
PLUGINVERSION = 2
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = octeon.Plugin()
@plugin.command(command="/cv",
                description="shows who's in the royal games discord server right now",
                inline_supported=False,
                hidden=False)
def cv(bot, update, user, args):
    r = requests.get('https://discordapp.com/api/guilds/176353500710699008/widget.json')
    data = ''
    if r.ok:
        data = r.json()
    else:
        return octeon.message(text="Problema con l'API discord!")
    message = '*Online in {}*'.format(data['name'])

    symbols = {'online': '🔵','dnd':'🔴', 'idle':'⚫', 'offline' :'⚪', 'deaf':'🔇', 'mute': '🔈', 'speaking': '🔊', 'music': '🎵', 'game': '🎮'}

    toremove= []
    notEmpty = set()
    for member in data['members']:
        if not "channel_id" in member:
            toremove.append(member)
        else:
            notEmpty.add(member['channel_id'])
    for member in toremove:
        data['members'].remove(member)

    channels = sorted(data['channels'], key=lambda canale: canale["position"])
    for channel in channels:
        if not channel['id'] in notEmpty:
            continue
        message+="\n\n{}:".format(channel['name'])
        for member in data['members']:
            if member['channel_id'] == channel['id']:
                message+="\n    "
                if member['self_deaf'] or member['deaf']:
                    message += symbols["deaf"]
                elif member['self_mute'] or member['mute']:
                    message+= symbols["mute"]
                else:
                    message+= symbols["speaking"]
                message += "{} {}".format(symbols[member['status']], member['username'])
                if "game" in member:
                    message+=" {} _{}_".format(symbols['game'], member['game']['name'])



    return octeon.message(text=message, parse_mode='Markdown')
