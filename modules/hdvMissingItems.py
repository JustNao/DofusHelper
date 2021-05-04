print('Importing sources ...')

from sniffer import protocol
from colorama import Fore
from pywinauto.findwindows import find_window
from win32 import win32gui
import win32com.client as client
from sources.item import gameItems, itemToName
print('Sources imported !')


def packetRead(msg):
    if msg.id == 7549:
        packet = protocol.read(protocol.msg_from_id[msg.id]["name"], msg.data)
        missingItems = []
        for item in gameItems[packet['objectType']]:
            if item not in packet['typeDescription']:
                missingItems.append(item)
                print(Fore.GREEN + itemToName[item] + Fore.RESET)
