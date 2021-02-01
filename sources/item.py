import json
from .id import i18n

with open('sources\\gameRessources\\Items.json', encoding='utf-8') as f:
    itemJs = json.load(f)

itemToName = {}
for item in itemJs:
    try:
        itemToName[item['id']] = i18n['texts'][str(item['nameId'])]
    except KeyError:
        pass