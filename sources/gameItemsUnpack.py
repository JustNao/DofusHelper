import json

with open('sources\\gameRessources\\Items.json', encoding='utf-8') as f:
    itemJs = json.load(f)

gameItems = {}
for item in itemJs:
    try:
        gameItems[item['typeId']].append({
            'id' : item['id'],
            'nameId' : item['nameId'],
            'level' : item['level'],
            'craftable': len(item['recipeIds']) > 0
            })
    except KeyError:
        gameItems[item['typeId']] = [
            {
            'id' : item['id'],
            'nameId' : item['nameId'],
            'level' : item['level'],
            'craftable': len(item['recipeIds']) > 0
            }
        ]
with open('sources/gameRessources/gameItems.json', 'w') as out:
    json.dump(gameItems, out)