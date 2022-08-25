import json

with open('sources\\gameRessources\\MapPositions.json', encoding='utf-8') as f:
    mapPositions = json.load(f)
with open('sources\\gameRessources\\i18n_fr.json', encoding='utf-8') as f:
    i18n = json.load(f)
with open('sources\\gameRessources\\textId.json', encoding='utf-8') as f:
    textId = json.load(f)
with open('sources\\gameRessources\\PointOfInterest.json', encoding='utf-8') as f:
    poiJs = json.load(f)
with open('sources\\gameRessources\\Npcs.json', encoding='utf-8') as f:
    npcJs = json.load(f)
with open('sources\\gameRessources\\Archi.json', encoding='utf-8') as f:
    archiNameList = json.load(f)
with open('sources\\gameRessources\\Monsters.json', encoding='utf-8') as f:
    monsterJs = json.load(f)

mapIdToCoords = {}
for k in mapPositions:
    mapIdToCoords[int(k['id'])] = [k['posX'], k['posY']]

poiToNameId = {}
for poi in poiJs:
    poiToNameId[poi['id']] = poi['nameId']

def poiToName(id):
    nameId = [obj for obj in poiJs if obj['id']==id][0]['nameId']
    try:
        name = i18n['texts'][str(nameId)]
    except KeyError:
        return "Unknown"
    return name

def npcToName(id):
    nameId = [obj for obj in npcJs if obj['id']==id][0]['nameId']
    try:
        name = i18n['texts'][str(nameId)]
    except KeyError:
        return "Unknown"
    return name

def monsterToName(id):
    try:
        nameId = [obj for obj in monsterJs if obj['id']==id][0]['nameId']
        name = i18n['texts'][str(nameId)]
        return name
    except KeyError:
        print("Couldn't identify", id)
        return ''