print('Importing sources ...')
from typing import ItemsView
from sniffer import protocol
from sources.item import runes, itemToName
from sources.effects import effects
from colorama import Fore
from ui.gui import ui
from typing import NewType
import json
print('Sources imported !')

# class Nomansland:
#     # Scan autopilotage HDV
#     def __init__(self) -> None:
#         self.items = []

#     def packetRead(self, msg):
#         name = protocol.msg_from_id[msg.id]["name"]
#         if name == "ExchangeTypesItemsExchangerDescriptionForUserMessage":
#             packet = protocol.readMsg(msg)
#             if packet is None:
#                 return
#             if len(packet['itemTypeDescriptions']) > 0 and packet['itemTypeDescriptions'][0]['objectGID'] not in self.items:
#                 self.items.append(packet['itemTypeDescriptions'][0]['objectGID'])
#                 for item in packet['itemTypeDescriptions']:
#                     if len(item['effects']) > 0 and 'capacities' in item['effects'][0] and 10 in item['effects'][0]['capacities']:
#                         print("Found a", itemToName[item['objectGID']], "at", kamasToString(item["prices"][0]) + 'K')

class Nomansland:
    # Forgemagie

    def __init__(self) -> None:
        self.items = []
        self.itemIds = []
        self.currentItem = None
        self.currentRune = None
        self.runeIds = [int(id) for id in runes]

    class Item:
        def __init__(self, id, state, reliquat = 0) -> None:
            self.id = id
            self.reliquat = reliquat
            self.state = state
            
        def updateReliquat(self, reliquat):
            self.reliquat += reliquat
            print("New reliquat :", self.reliquat)
        
        def updateState(self, state):
            self.state = state
        
    def addItem(self, id, state):
        self.items.append(self.Item(id, state))
        self.itemIds.append(id)
        self.currentItem = self.items[-1]
        print("Added item " + Fore.CYAN + itemToName[id] + Fore.RESET)
    
    def addRune(self, id):
        self.currentRune = id
        print("Added rune " + itemToName[id] + " : " + str(runes[str(id)]['poids']))

    def packetRead(self, msg):
        name = protocol.msg_from_id[msg.id]["name"]
        packet = protocol.readMsg(msg)
        if name == "ExchangeObjectAddedMessage":
            if packet['object']['objectGID'] not in self.runeIds and packet['object']['objectGID'] not in self.itemIds :
                self.addItem(packet['object']['objectGID'], packet['object']['effects'])
            elif packet['object']['objectGID'] in self.runeIds:
                self.addRune(packet['object']['objectGID'])
        elif name == "ExchangeCraftResultMagicWithObjectDescMessage":
            # craftResult :
            # 1 -> Echec
            # 2 -> Succès
            # magicPoolStatus :
            # 1 -> Equivalence
            # 2 -> Gain reliquat
            # 3 -> Perte reliquat
            if packet['magicPoolStatus'] == 1:
                self.currentItem.updateState(packet['objectInfo']['effects'])
                print("Equivalence")
            else:
                if packet['craftResult'] == 1 and packet['magicPoolStatus'] == 3:
                    reliquatDif = round(-1*runes[str(self.currentRune)]['poids'], 1)
                else:
                    reliquatDif = 0
                print(str(reliquatDif) + " + ", end='')
                for index, stat in enumerate(self.currentItem.state):
                    try:
                        statDif = packet['objectInfo']['effects'][index]['value'] - stat['value']
                    except IndexError:
                        statDif = 0 - stat['value']
                    if statDif != 0:
                        effect = effects(stat['actionId'])
                        if effect['operator'] == "+":
                            reliquatDif += round(-1*effect['reliquat']*statDif, 1)
                            print(str(round(-1*effect['reliquat']*statDif, 1)) + " + ", end='')
                        else:  
                            reliquatDif += effect['reliquat']*statDif
                            print(str(round(effect['reliquat']*statDif, 1)) + " + ", end='')
                print(" =", reliquatDif)
                self.currentItem.updateReliquat(reliquatDif)
                self.currentItem.updateState(packet['objectInfo']['effects'])
