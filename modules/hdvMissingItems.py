print('Importing sources ...')

from sniffer import protocol
from colorama import Fore
from sources.item import gameItems, itemToName
print('Sources imported !')


def packetRead(msg):
    if msg.id == 7549:
        packet = protocol.read(protocol.msg_from_id[msg.id]["name"], msg.data)
        missingItems = []
        for item in gameItems[str(packet['objectType'])]:
            if item['id'] not in packet['typeDescription'] and item['craftable']:
                missingItems.append(item)
                print(Fore.BLUE + str(item['level']) + " " + Fore.GREEN + itemToName[item['id']] + Fore.RESET)
