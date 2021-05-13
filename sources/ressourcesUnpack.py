import json

with open('sources\\gameRessources\\Items.json', encoding='utf-8') as f:
    itemJs = json.load(f)

gameItems = {}
effects = {
    111: 'PA',
    128: 'PM',
    117: 'PO',
    182: 'Invoc',
    219: '% Neutre',
    214: '% Neutre',
    210: '% Terre',
    215: '% Terre',
    211: '% Eau',
    216: '% Eau',
    212: '% Air',
    217: '% Air',
    213: '% Feu',
    218: '% Feu',
    2804: 'Do Dist',
    # 160: 'Esquive PA',
    # 161: 'Esquive PM',
    412: 'Retrait PM',
    755: 'Tacle',
    753: 'Tacle',
    422: 'Do Terre',
    423: 'Do Terre',
    425: 'Do Feu',
    424: 'Do Feu',
    429: 'Do Air',
    428: 'Do Air',
    426: 'Do Eau',
    427: 'Do Eau',
    418: 'Do Crit',
    419: 'Do Crit',
    430: 'Do Neutre',
    431: 'Do Neutre'
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