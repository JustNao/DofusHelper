print('Importing sources ...')

from .pricesListing import kamasToString, craftPrice
from pyasn1.type.univ import Boolean
from sniffer import protocol
import time, datetime
from colorama import Fore
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sources.item import gameItems, itemToName, ressourcesId, recipes, prices
print('Sources imported !')

# Print iterations progress
requestCount = 0
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    global requestCount
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    requestCount += 1
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

class MissingItemLookup:
    def __init__(self, gui) -> Boolean:
        # use creds to create a client to interact with the Google Drive API
        scope = ['https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('access/client_secret.json', scope)
        self._client = gspread.authorize(creds)
        self._alreadyMissingItems = {}

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        self._spreadSheet = self._client.open("Missing Items")

        # Extract and print all of the values
        infos = self._spreadSheet.worksheet("Infos").get_all_records()
        lastSave = infos[0]['Last save']
        self._workSheets = self._spreadSheet.worksheets()

        self._currentDateFormatted = str(datetime.datetime.today().strftime ('%d-%m-%Y')) # format the date to ddmmyyyy
        self._isCurrentDay = (lastSave == self._currentDateFormatted)
        if self._isCurrentDay:
            self.overWrite = gui.overWrite()
            if self.overWrite:
                # t = threading.Thread(target=self.moduleInitialization, name="Module Initialization")
                # t.start()
                self.moduleInitialization()
            else:
                gui.abortWindow()
        else:
            self.moduleInitialization()

    def moduleInitialization(self):
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
                self._missingItems[type] = {}

        countTypes = len(self._missingItems)
        print(Fore.YELLOW + "Getting old items" + Fore.RESET)
        printProgressBar(0, countTypes, prefix = 'Progress:', suffix = 'Received', length = 50)
        ind = 1
        for sheetIndex in range(countTypes):
            sheet = self._workSheets[sheetIndex]
            self._alreadyMissingItems[sheet.title] = sheet.get_all_records()
            printProgressBar(ind, countTypes, prefix = 'Progress:', suffix = 'Received', length = 50)
            ind += 1
        self.abort = False
        return False
    
    def _indexOf(self, nameToLookFor, dictList):
        index = 0
        for item in dictList:
            if item['Nom'] == nameToLookFor:
                return index
            else:
                index += 1
        return -1

    def _idsFromType(self, inputType):
        ids = []
        for intType, strType in self._idToType.items():
            if strType == inputType:
                ids.append(intType)
        return ids
        
    def packetRead(self, msg):
        if msg.id == 7549:
            packet = protocol.read(protocol.msg_from_id[msg.id]["name"], msg.data)
            if packet['objectType'] not in self._idToType.keys():
                return
            for item in gameItems[str(packet['objectType'])]:
                if item['id'] not in packet['typeDescription'] and item['craftable']:
                    self._missingItems[self._idToType[packet['objectType']]][item['id']] = item
            print("Catégorie " + Fore.CYAN + self._idToType[packet['objectType']] + Fore.RESET + " ajoutée")    

    def saveMissingItems(self):
        global requestCount
        # Failsafe
        for itemType in self._missingItems.keys():
            if len(self._missingItems[itemType]) == 0:
                return

        typeProgress = 0
        requestCount = 0
        countTypes = len(self._missingItems)
        print(Fore.YELLOW + "Sending new items" + Fore.RESET)
        printProgressBar(0, countTypes, prefix = 'Progress:', suffix = 'Sent', length = 50)
        for itemType, itemList in self._missingItems.items():
            newRows = []
            oldRows = {}
            updateRows = []
            deleteRows = []
            # Selecting old items that will be deleted (not missing anymore)
            rowToDelete = 1
            for itemAlreadyMissing in self._alreadyMissingItems[itemType]:
                for id in self._idsFromType(itemType):
                    for dbItem in gameItems[str(id)]:
                        if itemToName[dbItem['id']] == itemAlreadyMissing['Nom']:
                            if not self._isCurrentDay:
                                dayCount = itemAlreadyMissing['Jours consécutifs'] + 1
                            else:
                                dayCount = itemAlreadyMissing['Jours consécutifs']
                            effects = ', '.join(dbItem['effects'])
                            price = kamasToString(craftPrice(dbItem['id']))
                            oldRows[self._indexOf(itemToName[dbItem['id']], self._alreadyMissingItems[itemType])] = [effects, price, dayCount]
                            break

            for item in itemList.values():
                # Check if the item is already missing
                alreadyMissing = False
                for itemAlreadyMissing in self._alreadyMissingItems[itemType]:
                    if itemAlreadyMissing['Nom'] == itemToName[item['id']]:
                        alreadyMissing = True
                        break
                if not alreadyMissing:
                    effects = ', '.join(item['effects'])
                    price = kamasToString(craftPrice(item['id']))
                    newRows.append(
                        [item['level'], itemToName[item['id']], effects, price,  0, ""]
                    )

            progress = 1

            for i in range(len(oldRows)):
                for itemIndex, itemToUpdate in oldRows.items():
                    if i == itemIndex:
                        updateRows.append(itemToUpdate)
                        break
            
            # for rowToDelete in deleteRows:
            #     self._spreadSheet.worksheet(itemType).delete_row(rowToDelete)
            #     printProgressBar((progress/(len(deleteRows) + 3)) + typeProgress, countTypes, prefix = 'Progress:', suffix = 'Sent', length = 50)
            #     progress += 1
            # self._spreadSheet.worksheet(itemType).delete_rows(2, len(self._alreadyMissingItems[itemType]))
            self._spreadSheet.worksheet(itemType).update("C2:E" + str(len(updateRows) + 1), updateRows)
            printProgressBar(0.5 + typeProgress, countTypes, prefix = 'Progress:', suffix = 'Sent', length = 50)
            progress += 1
            self._spreadSheet.worksheet(itemType).insert_rows(newRows, row = 2 + len(oldRows))
            printProgressBar(1 + typeProgress, countTypes, prefix = 'Progress:', suffix = 'Sent', length = 50)
            typeProgress += 1
        self._spreadSheet.worksheet("Infos").update_cell(2, 1, self._currentDateFormatted)
        printProgressBar(countTypes, countTypes, prefix = 'Progress:', suffix = 'Sent', length = 50)
