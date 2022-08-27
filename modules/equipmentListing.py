import os
import sys
import locale
from .pricesListing import kamasToString
from random import random
from ui.gui import ui
from sources.item import gameItems, itemToName
from math import pow, ceil
from time import sleep
import threading
import json
import pyperclip
import pyautogui as ag
import win32com.client as client
from win32 import win32gui
from colorama import Fore
from sniffer import protocol
from typing import Type
print('Importing sources ...')

print('Sources imported !')

locale.setlocale(locale.LC_ALL, '')
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))


class EquipmentListing:
    def __init__(self) -> None:
        with open('sources/gameRessources/equipmentPrices.json', 'r') as inFile:
            self._ressourcesPrice = json.load(inFile)
            inFile.close()
        self._posSearch = None
        self.MIN_LEVEL = 170
        self.idToType = {
            1: 'Amulette',
            9: 'Anneau',
            10: 'Ceinture',
            11: 'Bottes',
            82: 'Bouclier',
            16: 'Coiffe',
            17: 'Cape',
            81: 'Cape',  # Sac à Dos
            2: 'Arme',  # Tous les types d'arme
            3: 'Arme',
            4: 'Arme',
            5: 'Arme',
            6: 'Arme',
            7: 'Arme',
            8: 'Arme',
            19: 'Arme',
            21: 'Arme',
            22: 'Arme',
            114: 'Arme',
            151: 'Trophée'
        }

        self._missingItems = []
        itemCount = 0
        for ressourceType in self.idToType:
            for item in gameItems[str(ressourceType)]:
                if str(item['id']) not in self._ressourcesPrice.keys() and (item['level'] >= self.MIN_LEVEL or ressourceType in (151,)):
                    self._missingItems.append(item['id'])
        print(len(self._missingItems))
        print(itemCount)

    def packetRead(self, msg):
        name = protocol.msg_from_id[msg.id]['name']
        if name == "ExchangeStartedBidBuyerMessage":
            packet = protocol.readMsg(msg)
            if packet is None or self._posSearch is not None:
                return
            sleep(2)
            try:
                self._posSearch = ag.locateCenterOnScreen(
                    application_path + '\\..\\sources\\img\\pixel\\hdvBuySearch.png', confidence=0.75)
                self._posClick = (
                    self._posSearch[0]*2, self._posSearch[1] + 20)
            except TypeError:
                print(
                    Fore.RED + 'Couldn\'t find the position to click. Is Dofus open ?' + Fore.RESET)
                return
            ag.PAUSE = 0.3
            t = threading.Thread(target=self.searchBot,
                                 name="Search Bot", args=(packet,))
            t.start()

        elif name == "ExchangeTypesItemsExchangerDescriptionForUserMessage":
            packet = protocol.readMsg(msg)
            if packet is None:
                return

            if len(packet['itemTypeDescriptions']) == 0 or packet['itemTypeDescriptions'][0]['objectGID'] not in self._missingItems:
                return

            avgPrice = 0
            div = 0
            packet['itemTypeDescriptions'].sort(key=lambda x: x['prices'][0])
            for unit in range(2, -1, -1):
                if packet['itemTypeDescriptions'][0]['prices'][unit] != 0:
                    if unit == 2:
                        # 100
                        coef = 6
                    elif unit == 1:
                        # 10
                        coef = 3
                    else:
                        # 1
                        coef = 1
                    avgPrice += packet['itemTypeDescriptions'][0]['prices'][unit] / \
                        pow(10, unit)*coef
                    div += coef

            avgPrice /= div
            avgPrice = ceil(avgPrice)

            self._ressourcesPrice[packet['itemTypeDescriptions']
                                  [0]['objectGID']] = avgPrice
            print("Adding", itemToName[packet['itemTypeDescriptions']
                  [0]['objectGID']], ":", kamasToString(avgPrice), "K")

    def searchBot(self, packet):
        count = 0
        try:
            for ressourceType in self.idToType:
                for item in gameItems[str(ressourceType)]:
                    if item['id'] in self._missingItems:
                        sleep(random()*0.75)
                        ui.changeText(str(count))
                        count += 1
                        ag.click(self._posSearch)
                        ag.hotkey("ctrl", "a")
                        ag.typewrite(['del'])
                        pyperclip.copy(itemToName[item['id']])
                        print(itemToName[item['id']])
                        ag.hotkey("ctrl", "v")
                        sleep(0.7)
                        ag.click(self._posClick)
                with open('sources/gameRessources/equipmentPrices.json', 'w') as outFile:
                    print("Saving ...")
                    json.dump(self._ressourcesPrice, outFile)
                    outFile.close()
        except:
            with open('sources/gameRessources/equipmentPrices.json', 'w') as outFile:
                print("Saving ...")
                json.dump(self._ressourcesPrice, outFile)
                outFile.close()
