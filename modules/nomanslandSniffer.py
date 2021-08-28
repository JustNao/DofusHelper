print('Importing sources ...')
from sniffer import protocol
from sources.id import monsterToName
from .pricesListing import kamasToString
from colorama import Fore
from ui.gui import ui
import json
print('Sources imported !')

class Nomansland:
    # Scan autopilotage HDV
    def __init__(self) -> None:
        self.items = []

    def packetRead(self, msg):
        name = protocol.msg_from_id[msg.id]["name"]
        if name == "ExchangeTypesItemsExchangerDescriptionForUserMessage":
            packet = protocol.readMsg(msg)
            if packet is None:
                return
            if len(packet['itemTypeDescriptions']) > 0 and packet['itemTypeDescriptions'][0]['objectGID'] not in self.items:
                self.items.append(packet['itemTypeDescriptions'][0]['objectGID'])
                for item in packet['itemTypeDescriptions']:
                    if len(item['effects']) > 0 and 'capacities' in item['effects'][0] and 10 in item['effects'][0]['capacities']:
                        print("Found a", itemToName[item['objectGID']], "at", kamasToString(item["prices"][0]) + 'K')
