"""
SMECDS
"""
import core, random
PLUGINVERSION = 2
# Always name this variable as `plugin`
# If you dont, module loader will fail to load the plugin!
plugin = core.Plugin()
stagismo = ["dello stagista", "degli sposi", "di Santinelli", "di Sensei", "di Steffo", "di Spaggia",
            "della sedia", "di Satana", "del Sangue (degli occhi di Adry)", "del Sale",
            "del Serpente", "della Samsung", "di smecds", "della succursale", "di succ",
            "di Sans", "di [SiivaGunner](https://www.youtube.com/channel/UC9ecwl3FTG66jIKA9JRDtmg)",
            "di saaaaaas", "del semaforo", "della Seriale", "di Sistemi", "della Supercell",
            "di Santaclaus", "dei Sims", "dei Santi", "di SES2017", "di Salvini", "della scolopendra"]
random.seed()
@plugin.message(regex="(?i).*(smecds)") # You pass regex pattern
def smecds(bot, update):
    ds = random.choice(stagismo)
    return core.message(text="Secondo me é colpa "+ds)
