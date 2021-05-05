import json

with open('sources\\gameRessources\\Items.json', encoding='utf-8') as f:
    itemJs = json.load(f)

gameItems = {}
effects = {
    111: 'PA',
    128: 'PM',
    117: 'PO',
    182: 'Invoc',
    # 210: '%% Terre',
    # 211: '%% Eau',
    # 212: '%% Air',
    # 213: '%% Feu',
    2804: 'Do Dist',
    160: 'Esquive PA',
    161: 'Esquive PM',
    412: 'Retrait PM',
}
for item in itemJs:
    interestingEffects = []
    for effect in item['possibleEffects']:
        if effect['effectId'] in effects.keys():
            interestingEffects.append(effects[effect['effectId']])
    try:
        gameItems[item['typeId']].append({
            'id' : item['id'],
            'nameId' : item['nameId'],
            'level' : item['level'],
            'craftable': item['recipeSlots'] > 0,
            'effects': interestingEffects
            })
    except KeyError:
        gameItems[item['typeId']] = [
            {
            'id' : item['id'],
            'nameId' : item['nameId'],
            'level' : item['level'],
            'craftable': item['recipeSlots'] > 0,
            'effects': interestingEffects
            }
        ]

with open('sources/gameRessources/gameItems.json', 'w') as out:
    json.dump(gameItems, out)