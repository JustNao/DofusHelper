print('Importing sources ...')

from typing import Type
from sniffer import protocol
from colorama import Fore
from win32 import win32gui
import win32com.client as client
import pyautogui as ag
import pyperclip
import json
import locale, sys, os
import threading
from time import sleep
from math import pow, ceil
from sources.item import gameItems, itemToName, ressourcesId, recipes, prices
from ui.gui import ui
from random import random
print('Sources imported !')

locale.setlocale(locale.LC_ALL, '')
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
def kamasToString(price: int):
    return f'{price:,}'

def craftPrice(item: int):
    craft = None
    for recipe in recipes:
        if recipe['resultId'] == item:
            craft = recipe
            break
    if craft == None:
        # print(Fore.YELLOW + "Item price missing for", itemToName[item] + Fore.RESET)
        return 0

    price = 0
    index = 0
    for ressource in craft['ingredientIds']:
        try:
            price += craft['quantities'][index]*prices[str(ressource)]
        except KeyError:
            ressourcePrice = craftPrice(ressource)
            if ressourcePrice == 0:
                return 0
            price += craft['quantities'][index]*craftPrice(ressource)
        index += 1
    
    if str(item) in prices and prices[str(item)] < price:
        # print("HDV price better for", itemToName[item], ":", price)
        return prices[str(item)]
    else:
        # print("Craft price for", itemToName[item], ":", price)
        return price

class PriceListing:
    def __init__(self) -> None:
        with open('sources/gameRessources/prices.json', 'r') as inFile:
            self._ressourcesPrice = json.load(inFile)
            inFile.close()
        self._posSearch = None
        self._missingItems = []
        itemCount = 0
        for ressourceType in ressourcesId:
                for ressource in gameItems[str(ressourceType)]:
                    if str(ressource['id']) not in self._ressourcesPrice.keys() and ressource['usedInCrafting']:
                        self._missingItems.append(ressource['id'])
        print(len(self._missingItems))
        print(itemCount)

    def packetRead(self, msg):
        # print(protocol.msg_from_id[msg.id]['name'], msg.id, sep=", ")
        if msg.id == 8765 : 
            # 8765, ExchangeStartedBidBuyerMessage
            packet = protocol.readMsg(msg)
            if packet is None or self._posSearch is not None:
                return
            sleep(2)
            try:
                self._posSearch = ag.locateCenterOnScreen(application_path + '\\..\\sources\\img\\pixel\\hdvBuySearch.png', confidence = 0.75)
                self._posClick = (self._posSearch[0]*2, self._posSearch[1] + 20)
            except TypeError:
                print(Fore.RED + 'Couldn\'t find the position to click. Is Dofus open ?' + Fore.RESET)
                return
            ag.PAUSE = 0.3
            t = threading.Thread(target=self.searchBot, name="Search Bot", args= (packet,))
            t.start()
            
        elif msg.id == 3270:
            # 3270, ExchangeTypesItemsExchangerDescriptionForUserMessage
            packet = protocol.readMsg(msg)
            if packet is None:
                return

            unitCount = 0
            if len(packet['itemTypeDescriptions']) == 0 or packet['itemTypeDescriptions'][0]['objectGID'] not in self._missingItems:
                return

            avgPrice = 0
            div = 0
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
                    avgPrice += packet['itemTypeDescriptions'][0]['prices'][unit]/pow(10, unit)*coef
                    div += coef
            
            avgPrice /= div        
            avgPrice = ceil(avgPrice)
            
            self._ressourcesPrice[packet['itemTypeDescriptions'][0]['objectGID']] = avgPrice
            print("Adding", itemToName[packet['itemTypeDescriptions'][0]['objectGID']], ":", avgPrice, "K")
    
    def searchBot(self, packet):
        count = 0
        way = input("Manuel (m) or automatic (a) ? ")
        if way == 'a':
            try:
                for ressourceType in ressourcesId:
                    for ressource in gameItems[str(ressourceType)]:
                        if ressource['id'] in self._missingItems:
                            sleep(random()*0.75)
                            ui.changeText(str(count))
                            count += 1
                            ag.click(self._posSearch)
                            ag.hotkey("ctrl", "a")
                            ag.typewrite(['del'])
                            pyperclip.copy(itemToName[ressource['id']])
                            print(itemToName[ressource['id']])
                            ag.hotkey("ctrl", "v")
                            sleep(2)
                            ag.click(self._posClick)
                            sleep(1)
                    with open('sources/gameRessources/prices.json', 'w') as outFile:
                        json.dump(self._ressourcesPrice, outFile)
                        outFile.close()
            except:
                with open('sources/gameRessources/prices.json', 'w') as outFile:
                    json.dump(self._ressourcesPrice, outFile)
                    outFile.close()
        else:
            for missingItem in self._missingItems:
                price = input(itemToName[missingItem] +  " : ")
                if price == '':
                    continue
                elif price == 'stop':
                    break
                if str(missingItem) not in self._ressourcesPrice:
                    self._ressourcesPrice[str(missingItem)] = int(price)
            
            with open('sources/gameRessources/prices.json', 'w') as outFile:
                    json.dump(self._ressourcesPrice, outFile)
                    outFile.close()
            