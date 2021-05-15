print('Importing sources ...')
from sniffer import protocol
from sources.item import itemToName
import pyautogui as ag
import os, sys, time
from collections import OrderedDict
from colorama import Fore
import pyperclip
from random import random
from ui.gui import ui
import locale
from math import pow, ceil, log
import PySimpleGUI as sg
print('Sources imported !')

locale.setlocale(locale.LC_ALL, '')
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

class Item:
    def __init__(self, quantity, price):
        self.count = [
            {'quantity': 0, 'postedPrice': 0}, 
            {'quantity': 0, 'postedPrice': 0}, 
            {'quantity': 0, 'postedPrice': 0}
        ]
        self.count[quantity]['quantity'] = 1
        self.count[quantity]['postedPrice'] = price
    
    def __str__(self):
        return str(self.count)

    def add(self, quantity, price):
        self.count[quantity]['quantity'] += 1
        if (price < self.count[quantity]['postedPrice']) or (self.count[quantity]['postedPrice'] == 0):
            self.count[quantity]['postedPrice'] = price

    def getSellsQuantity(self) -> int:
        count = 0
        for unit in self.count:
            count += unit['quantity']
        return count

def getColors(data):
    index = 0
    colors = []
    for item in data:
        difPercentage = int(item[-1][:-1])
        if difPercentage == 0:
            color = 'LightBlue'
        elif difPercentage < 5:
            color = 'green'
        elif difPercentage < 15:
            color = 'yellow'
        else:
            color = 'orange'
        colors.append((index, color))
        index += 1
    return colors

def dataSells(sells):
    def sortPercentage(item):
        return int(item[-1][:-1])

    data = [[j for j in range(8)] for i in range(len(sells))]

    i = 0
    for key in sellsList:
        item = key[1]
        data[i][0] = item['name']
        indData = 0
        minDif = 0
        difPercentage = 0
        for j in range(3):
            indData += 1
            data[i][indData] = '{:n}'.format(item['playerAmount'].count[j]['postedPrice'])
            indData += 1
            data[i][indData] = '{:n}'.format(item['hdvAmount'][j])
            if item['playerAmount'].count[j]['postedPrice'] != 0:
                dif = abs(item['playerAmount'].count[j]['postedPrice'] - item['hdvAmount'][j])
                if dif > minDif:
                    minDif = dif
                    difPercentage = ceil(dif/item['playerAmount'].count[j]['postedPrice']*100)
        sells[key[0]]['dif'] = difPercentage
        data[i][7] = str(difPercentage) + '%'
        i += 1
    data.sort(key = sortPercentage, reverse = True)
    return data

def getCurrentSells(packet):
    global sells
    sells = OrderedDict()
    for object in packet['objectsInfos']:
        ind = int(log(object['quantity'], 10))
        try:
            sells[object['objectGID']]['playerAmount'].add(quantity = ind, price = object['objectPrice'])
        except KeyError:
            sells[object['objectGID']] = {
                                            'name' : itemToName[object['objectGID']],
                                            'playerAmount' : Item(quantity = ind, price = object['objectPrice'])
            }
    newSells = sells.copy()
    # Checking if item names are similar, in which case some problems may occur down the line
    for firstItem in sells:
        for secondItem in sells:
            if (secondItem in newSells) and (firstItem != secondItem) and ((itemToName[firstItem] in itemToName[secondItem]) or (itemToName[secondItem] in itemToName[firstItem])):
                newSells.pop(secondItem)
    
    sells = newSells
    for key in sells:
        print(str(key) + ' : ' + str(sells[key]))

def getCurrentPrice(packet):
    if not 'hdvAmount' in sells[packet['genericId']]:
        sells[packet['genericId']]['hdvAmount'] = packet['minimalPrices']
    setNewPrice()

def packetRead(msg):
    global sellsList, index, posSearch, sellInfoPos, middleElementPos, selectPos
    if msg.id == 8157:
        # ExchangeStartedSellerMessage
        packet = protocol.readMsg(msg)
        if packet is None:
            return
        time.sleep(1)
        middleElementPos = ag.locateCenterOnScreen(application_path + '\\..\\sources\\img\\pixel\\hdvMiddleElement.png', confidence = 0.75)
        try:
            posSearch = (middleElementPos[0], middleElementPos[1] - 40)
            sellInfoPos = (middleElementPos[0], middleElementPos[1] + 40 )
        except TypeError:
            print(Fore.RED + 'Couldn\'t find the position to click. Is Dofus open ?' + Fore.RESET)
            return
        ag.PAUSE = 0.3
        selectPos = ag.locateCenterOnScreen(application_path + '\\..\\sources\\img\\pixel\\hdvSellItemClick.png', region = (sellInfoPos[0], sellInfoPos[1] - 20, 250, 40), grayscale = True, confidence = 0.75)
        try:
            ag.click(ag.locateOnScreen(application_path + '\\..\\sources\\img\\pixel\\lot.png'), interval = 0.05)
        except AttributeError:
            pass
        getCurrentSells(packet)
        sellsList = list(sells.items())
        ui.changeText(sellsList[0][1]['name'])
        time.sleep(1)
        print(Fore.YELLOW + "Starting item price update" + Fore.RESET)
        index = 0
        time.sleep(random()/2)
        ag.click(posSearch)
        time.sleep(0.5)
        ag.hotkey("ctrl", "a")
        ag.hotkey("ctrl", "a")
        ag.typewrite(['del'])
        pyperclip.copy(sellsList[0][1]['name'])
        ag.hotkey("ctrl", "v")
        time.sleep(1)
        ag.click(sellInfoPos)

    elif msg.id == 4848:
        # ExchangeBidPriceForSellerMessage
        packet = protocol.read(protocol.msg_from_id[msg.id]["name"], msg.data)
        getCurrentPrice(packet)

def warningPopup(self):
        sg.Popup('WARNING', 'L\'item va être posté à un prix très éloigné du prix moyen estimé. Etes-vous sûr de vouloir le poster à ce prix ?')

def setNewPrice():
    global index
    try:
        item = sellsList[index][1]
        ui.changeText(sellsList[index][1]['name'] + " (" + str(index + 1) + "/" + str(len(sellsList)) + ")")
    except IndexError:
        return

    if not "hdvAmount" in item:
        return
    itemCount = 0
    positionShift = 0
    firstItem = True
    abort = False
    for unit in range(2,-1,-1):
        if abort:
            break
        unitCount = 0
        if (item['playerAmount'].count[unit]['quantity'] == 0) or (item['playerAmount'].count[unit]['postedPrice'] - item['hdvAmount'][unit] == 0):
            for i in range(item['playerAmount'].count[unit]['quantity']):
                positionShift += 43
                itemCount += 1
            continue
        else:
            if not firstItem:
                ag.click(posSearch)
                time.sleep(0.5)
                ag.hotkey("ctrl", "a")
                ag.hotkey("ctrl", "a")
                ag.typewrite(['del'])
                pyperclip.copy(item['name'])
                ag.hotkey("ctrl", "v")
                time.sleep(1)
            firstItem = False
            initialUnitPositionShift = positionShift
            for i in range(item['playerAmount'].count[unit]['quantity']):
                ag.click(selectPos[0], selectPos[1] + positionShift)
                positionShift += 43
                itemCount += 1
                unitCount += 1
                if (itemCount >= 15):
                    break
            newPrice = item['hdvAmount'][unit] - 1
            print('Changing', Fore.YELLOW + str(item['playerAmount'].count[unit]['quantity']*pow(10, unit)) + Fore.RESET, 'units of', Fore.YELLOW + item['name'] + Fore.RESET, 'to', Fore.YELLOW + str('{:n}'.format(newPrice)) + 'K' + Fore.RESET)
            ag.typewrite(str(newPrice), interval = 0.05)
            ag.typewrite(['return'])
            
            warned = False
            if (ag.locateOnScreen(application_path + '\\..\\sources\\img\\pixel\\warning.png') is not None):
                print(Fore.RED + 'WARNING : price is very far from the estimated one. Do you confirm using the new price ?' + Fore.RESET)
                warned = True
            while (ag.locateOnScreen(application_path + '\\..\\sources\\img\\pixel\\warning.png') is not None):
                time.sleep(0.5)
            
            skipItem = "n"
            if warned:
                skipItem = input("Do you want to skip the item ? y/n\n")
            if skipItem == "y":
                abort = True
                positionShift = initialUnitPositionShift
                for i in range(item['playerAmount'].count[unit]['quantity']):
                    ag.click(selectPos[0], selectPos[1] + positionShift)
                    positionShift += 43
                break

            searchIndex = 0
            ouiPos = None
            while (ouiPos is None) and (searchIndex < 5):
                searchIndex += 1
                time.sleep(0.2)
                ouiPos = ag.locateOnScreen(application_path + '\\..\\sources\\img\\pixel\\oui.png', confidence = 0.75)
            if ouiPos is not None:
                ag.click(ouiPos)
        time.sleep(unitCount*0.5 + random()/2)


    index += 1
    if index >= len(sellsList):
        # If it's the last item, don't need to load the next
        ui.changeText("No more items")
        return
    ag.click(posSearch)
    time.sleep(0.5)
    ag.hotkey("ctrl", "a")
    ag.hotkey("ctrl", "a")
    ag.typewrite(['del'])
    pyperclip.copy(sellsList[index][1]['name'])
    ag.hotkey("ctrl", "v")
    time.sleep(0.5)
    ag.click(sellInfoPos)