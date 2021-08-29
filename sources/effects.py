import json

with open('sources\\gameRessources\\Effects.json', encoding='utf-8') as f:
    effectsJs = json.load(f)

def effects(id):
    for effect in effectsJs:
        if effect['id'] == id:
            return {
                "operator": effect["operator"],
                "reliquat": effect["effectPowerRate"],
            }
    return None