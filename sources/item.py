from .id import i18n
import json

with open('sources\\gameRessources\\Items.json', encoding='utf-8') as f:
    itemJs = json.load(f)

with open('sources\\gameRessources\\gameItems.json', encoding='utf-8') as f:
    gameItems = json.load(f)

itemToName = {}
for item in itemJs:
    try:
        itemToName[item['id']] = i18n['texts'][str(item['nameId'])]
    except KeyError:
        pass