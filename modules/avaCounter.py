print('Importing sources ...')

from sniffer import protocol
from colorama import Fore
from pywinauto.findwindows import find_window
from win32 import win32gui
import win32com.client as client
print('Sources imported !')


def packetRead(msg):
    if msg.id == 2291:
        charactersOnMap = {}
        packet = protocol.read(protocol.msg_from_id[msg.id]["name"], msg.data)
        for perso in packet['actors']:
            try:
                for option in perso['humanoidInfo']['options']:
                    if option['__type__'] == 'HumanOptionAlliance':
                        if option['allianceInformations']['allianceTag'] in charactersOnMap:
                            charactersOnMap[option['allianceInformations']['allianceTag']] += 1
                        else:
                            charactersOnMap[option['allianceInformations']['allianceTag']] = 1
            except KeyError:
                continue
        print(charactersOnMap)