from .id import i18n
import json

with open('sources\\gameRessources\\gameItems.json', encoding='utf-8') as f:
    gameItems = json.load(f)

with open('sources\\gameRessources\\Recipes.json', encoding='utf-8') as f:
    recipes = json.load(f)

with open('sources\\gameRessources\\prices.json', encoding='utf-8') as f:
    prices = json.load(f)

itemToName = {}
for key in gameItems:
    try:
        for item in gameItems[key]:
            itemToName[item['id']] = i18n['texts'][str(item['nameId'])]
    except KeyError:
        pass

ressourcesId = {
    104: "Aile",
    40: "Alliage",
    38: "Bois",
    108: "Bourgeon",
    107: "Carapace",
    34: "Céréale",
    119: "Champignon",
    111: "Coquille",
    56: "Cuir",
    96: "Ecorce",
    167: "Essence de gardien de donjon",
    55: "Etoffe",
    35: "Fleur",
    46: "Fruit",
    152: "Galet",
    110: "Gelée",
    58: "Graine",
    60: "Huile",
    57: "Laine",
    68: "Légume",
    228: "Liquide",
    71: "Matériel d'alchimie",
    195: "Matériel d'exploration",
    66: "Matéria",
    39: "Minerai",
    109: "Oeil",
    105: "Oeuf",
    106: "Oreille",
    47: "Os",
    103: "Patte",
    59: "Peau",
    51: "Pierre brute",
    50: "Pierre précieuse",
    95: "Planche",
    36: "Plante",
    53: "Plume",
    54: "Poil",
    41: "Poisson",
    48: "Poudre",
    179: "Préparation",
    65: "Queue",
    98: "Racine",
    229: "Ressource de combat",
    219: "Ressources des Songes",
    15: "Ressources diverses",
    185: "Sève",
    183: "Substrat",
    70: "Teinture",
    164: "Vêtement",
    63: "Viande"
}