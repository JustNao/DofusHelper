print('Importing sources ...')

from sniffer import protocol
from openpyxl import load_workbook
from itertools import islice
import time, datetime
from colorama import Fore
from sources.item import gameItems, itemToName
print('Sources imported !')


class MissingItemLookup:
    def __init__(self) -> None:
        self._filename = 'output/missingItems.xlsx'
        self._wb = load_workbook(self._filename)
        self._alreadyMissingItems = {}

        currentDateFormatted = str(datetime.datetime.today().strftime ('%d-%m-%Y')) # format the date to ddmmyyyy
        self._isCurrentDay = (self._wb['Coiffe']['I1'].value == currentDateFormatted)
        
        for sheetName in self._wb.sheetnames:
            self._wb[sheetName]['I1'].value = currentDateFormatted
            sheet = self._wb[sheetName]
            self._alreadyMissingItems[sheetName] = []
            for row in islice(sheet.values, 1, sheet.max_row):
                if row[0] == "Level":
                    continue
                else:  
                    self._alreadyMissingItems[sheetName].append(
                        {
                            'level': row[0],
                            'name': row[1],
                            'stats': row[2],
                            'days': row[3]
                        }
                    )
        self._idToType = {
            1: 'Amulette',
            9: 'Anneau',
            10: 'Ceinture',
            11: 'Bottes',
            82: 'Bouclier',
            16: 'Coiffe',
            17: 'Cape',
            81: 'Cape', # Sac à Dos
            2: 'Arme', # Tous les types d'arme
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

        self._missingItems = {}
        for type in self._idToType.values():
            try:
                self._missingItems[type]
            except KeyError:
                self._missingItems[type] = []
    def packetRead(self, msg):
        if msg.id == 7549:
            packet = protocol.read(protocol.msg_from_id[msg.id]["name"], msg.data)
            if packet['objectType'] not in self._idToType.keys():
                return
            for item in gameItems[str(packet['objectType'])]:
                if item['id'] not in packet['typeDescription'] and item['craftable']:
                    self._missingItems[self._idToType[packet['objectType']]].append(item)
            print("Catégorie " + Fore.CYAN + self._idToType[packet['objectType']] + Fore.RESET + " ajoutée")    
    def saveMissingItems(self):
        if not self._isCurrentDay:
            print(Fore.LIGHTMAGENTA_EX + "Getting old items" + Fore.RESET)
        for itemType, itemList in self._missingItems.items():
            currentRow = 2
            for item in itemList:
                dayCount = 0

                #  Checking if the item was already missing, only if it's not the same day
                for itemAlreadyMissing in self._alreadyMissingItems[itemType]:
                    if itemAlreadyMissing['name'] == itemToName[item['id']]:
                        if not self._isCurrentDay:
                            dayCount = itemAlreadyMissing['days'] + 1
                        else:
                            dayCount = itemAlreadyMissing['days']
                        break
                
                effects = ', '.join(item['effects'])
                self._wb[itemType]['A' + str(currentRow)].value = item['level']
                self._wb[itemType]['B' + str(currentRow)].value = itemToName[item['id']]      
                self._wb[itemType]['C' + str(currentRow)].value = effects      
                self._wb[itemType]['D' + str(currentRow)].value = dayCount
                currentRow += 1
            self._wb[itemType].delete_rows(currentRow, 200)
        saved = False
        while not saved:
            try:
                self._wb.save(self._filename)
                saved = True
                print(Fore.GREEN + "File saved" + Fore.RESET)
            except PermissionError:
                print(Fore.RED + "Can't save the file, please close it" + Fore.RESET)
                time.sleep(2)

