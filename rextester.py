import core
from bs4 import BeautifulSoup
from io import BytesIO
from base64 import b64decode
import html
import requests
import logging
LOGGER = logging.getLogger("RexTester")
PLUGINVERSION = 2
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = core.Plugin()
HEADERS = {"User-Agent":"Octeon/1.0"}
def get_langs():
    r = requests.get("http://rextester.com/main", headers=HEADERS)
    if r.ok:
        r = r.text
        r = BeautifulSoup(r, "html.parser")
        lang_list_pre = r.find_all("pre")[-2].text.split("\n")
        lang_list = {}
        for item in lang_list_pre:
            item = item.strip().split(" = ")
            if len(item) == 2:
                lang_list[item[0].replace(" ", "").lower()] = item[1]
        return lang_list
    else:
        raise Exception("Cant get language list")

LANGS = get_langs()
LOGGER.info("Rextester available languages:%s", LANGS)
LANG_LIST_STR = ""
for lang in LANGS:
    LANG_LIST_STR += lang + ", "
LOCALE_STR = core.locale.get_locales_dict("rextester")
@plugin.command(command="/rextester",
                description="Runs code on rextester.com(language list=http://rextester.com/main). Supply language as first argument. Use /rextester getlangs for list of languages",
                inline_supported=True,
                hidden=False,
                required_args=1)
def rt(bot, update, user, args):
    _ = lambda x: core.locale.get_localized(x, update.message.chat.id)
    args[0] = args[0].lower()
    if args[0] == "getlangs":
        return core.message(_(LOCALE_STR["available_langs"]) % LANG_LIST_STR, parse_mode="HTML")
    elif len(args) == 1:
        return core.message(_(LOCALE_STR["not_enough_arguments"]), failed=True, parse_mode="HTML")
    elif len(args) >= 2:
        if args[0] in LANGS:
            code = " ".join(args[1:]).split("/stdin")
            if len(code) == 2:
                stdin = code[1]
            else:
                stdin = ""
            program = code[0].rstrip("\n")
            r = requests.post("http://rextester.com/rundotnet/api",
                data={
                    "LanguageChoice":LANGS[args[0]],
                    "Program":program,
                    "Input":stdin
                })
            if r.ok:
                r = r.json()
                LOGGER.debug(r)
                resp = []
                for key, value in r.items():
                    if key.lower() in LOCALE_STR and value:
                        if not (key == "Result" and args[0] == "octave"):
                            resp.append(_(LOCALE_STR[key.lower()]) + ":\n<code>%s</code>\n" % html.escape(value.rstrip("\n")))
                if r["Files"]:
                    graph = BytesIO(b64decode(r["Files"][0]))
                else:
                    graph = None
                return core.message("\n".join(sorted(resp)), parse_mode="HTML", photo=graph)
            else:
                return core.message(text=_(LOCALE_STR["rextester_problems"]))
        else:
            return core.message(text=_(LOCALE_STR["unknown_lang"]) % args[0], failed=True, parse_mode='HTML')
