import json
from sources.id import monsterToName

with open('safekeep.json', encoding='utf-8') as f:
    hdvRequest = json.load(f)
with open('sources/gameRessources/Archi.json', 'r', encoding='utf-8') as arch:
    archimonstres = json.load(arch)

for group in hdvRequest['itemTypeDescriptions']:
    if len(group['effects']) == 1 or (len(group['effects']) == 2 and group['effects'][1]['__type__'] != "ObjectEffectDice"):
        archi = group['effects'][0]['diceConst']
        if monsterToName(archi) not in archimonstres:
            print(archi)
            archimonstres.append(monsterToName(archi))

with open('sources/archimonstres.json', 'w', encoding='utf-8') as outFile:
    json.dump(sorted(archimonstres), outFile, ensure_ascii=False)
    print("Loaded archimonstres")