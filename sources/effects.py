import json

with open('sources\\gameRessources\\Effects.json', encoding='utf-8') as f:
    effectsJs = json.load(f)

with open('sources\\gameRessources\\i18n_fr.json', encoding='utf-8') as f:
    i18n = json.load(f)

def effects(id):
    for effect in effectsJs:
        if effect['id'] == id:
            return {
                "operator": effect["operator"],
                "reliquat": effect["effectPowerRate"],
            }
    return None


idToEffect = {}
for effect in effectsJs:
    try:
        idToEffect[effect['id']] = {
            "operator": effect["operator"],
            "description": i18n['texts'][str(effect["descriptionId"])],
            "characteristic": effect["characteristic"],
        }
    except KeyError:
        pass
