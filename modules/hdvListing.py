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
    for key in sells:
        print(str(key) + ' : ' + str(sells[key]))

def getCurrentPrice(packet):
    global index, sells
    sells[packet['genericId']]['hdvAmount'] = packet['minimalPrices']
    ui.updateProgressBar((index/len(sells)*100))
    try:
        ag.click(posSearch)
        ag.hotkey("ctrl", "a")
        ag.typewrite(['del'])
        pyperclip.copy(sellsList[index][1]['name'])
        ag.hotkey("ctrl", "v")
        time.sleep(random()/4)
        ag.click(sellInfoPos)
        index += 1
    except IndexError:
        print(Fore.GREEN + "Finished listing all prices" + Fore.RESET)
        data = dataSells(sells)
        colors = getColors(data)
        ui.dataUpdate(data, colors)

def packetRead(msg):
    global sellsList, index, posSearch, sellInfoPos, middleElementPos
    if msg.id == 3101:
        packet = protocol.read(protocol.msg_from_id[msg.id]["name"], msg.data)
        getCurrentSells(packet)
        index = 1
        sellsList = list(sells.items())
        time.sleep(1.5)
        print(Fore.YELLOW + "Starting to look for prices ..." + Fore.RESET)
        middleElementPos = ag.locateCenterOnScreen(application_path + '\\..\\sources\\img\\pixel\\hdvMiddleElement.png', confidence = 0.75)
        try:
            posSearch = (middleElementPos[0], middleElementPos[1] - 40)
            sellInfoPos = (middleElementPos[0], middleElementPos[1] + 40 )
        except TypeError:
            print(Fore.RED + 'Couldn\'t find the position to click. Is Dofus open ?' + Fore.RESET)
            return
        ag.click(posSearch)
        time.sleep(1)
        pyperclip.copy(sellsList[0][1]['name'])
        ag.hotkey("ctrl", "v")
        ag.click(sellInfoPos)

    elif msg.id == 2041:
        packet = protocol.read(protocol.msg_from_id[msg.id]["name"], msg.data)
        getCurrentPrice(packet)

def automatePrices(threshold):
    index = 0
    ag.PAUSE = 0.3
    selectPos = ag.locateCenterOnScreen(application_path + '\\..\\sources\\img\\pixel\\hdvSellItemClick.png', region = (sellInfoPos[0], sellInfoPos[1] - 20, 250, 40), grayscale = True, confidence = 0.75)
    try:
        ag.click(ag.locateOnScreen(application_path + '\\..\\sources\\img\\pixel\\lot.png'), clicks = 2, interval = 0.05)
    except AttributeError:
        pass
    for key in sellsList:
        item = key[1]
        if item['dif'] > threshold :
            time.sleep(random()/2)
            positionShift = 0
            itemNumber = 0
            for unit in range(2,-1,-1):
                if (item['playerAmount'].count[unit]['quantity'] == 0) or (item['playerAmount'].count[unit]['postedPrice'] - item['hdvAmount'][unit] == 0):
                    continue
                else:
                    ag.click(posSearch)
                    time.sleep(0.5)
                    ag.hotkey("ctrl", "a")
                    ag.hotkey("ctrl", "a")
                    ag.typewrite(['del'])
                    pyperclip.copy(item['name'])
                    ag.hotkey("ctrl", "v")
                    for i in range(item['playerAmount'].count[unit]['quantity']):
                        ag.click(selectPos[0], selectPos[1] + positionShift)
                        positionShift += 43
                        itemNumber += 1
                        if (itemNumber == 15):
                            break
                    newPrice = item['hdvAmount'][unit] - 1
                    print('Changing', Fore.YELLOW + str(item['playerAmount'].count[unit]['quantity']*pow(10, unit)) + Fore.RESET, 'units of', Fore.YELLOW + item['name'] + Fore.RESET, 'to', Fore.YELLOW + str('{:n}'.format(newPrice)) + 'K' + Fore.RESET)
                    ag.typewrite(str(newPrice), interval = 0.05)
                    ag.typewrite(['return'])
                    
                    if (ag.locateOnScreen(application_path + '\\..\\sources\\img\\pixel\\warning.png') is not None):
                        ui.warningPopup()
                        print(Fore.RED + 'WARNING : price is very far from the estimated one. Do you confirm using the new price ?' + Fore.RESET)

                    while (ag.locateOnScreen(application_path + '\\..\\sources\\img\\pixel\\warning.png') is not None):
                        time.sleep(0.5)

                    searchIndex = 0
                    ouiPos = None
                    while (ouiPos is None) and (searchIndex < 5):
                        searchIndex += 1
                        time.sleep(0.1)
                        ouiPos = ag.locateOnScreen(application_path + '\\..\\sources\\img\\pixel\\oui.png')
                    if ouiPos is not None:
                        ag.click(ouiPos)
        index += 1
        ui.updateProgressBar((index/len(sells)*100))
    print(Fore.GREEN + 'Item pricing done !' + Fore.RESET)