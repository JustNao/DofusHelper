from tkinter import TclError
from tkinter.constants import CENTER, DISABLED, RIGHT, LEFT
from sniffer.network import flushBuffers
import PySimpleGUI as sg
import os, sys
import threading
import pyautogui as ag
from colorama import Fore
import time


class GraphicalInterface():
    def __init__(self, startSniff):
        self.found = None
        self.packetRead = None
        self.startSniff = startSniff
        self.stopSniff = None
        self.botting = True
        self._abortWindow = False
        sg.LOOK_AND_FEEL_TABLE['TreasureHunt'] = {'BACKGROUND': '#d4c194',
                                                  'TEXT': 'black',
                                                  'INPUT': '#DDE0DE',
                                                  'SCROLL': '#E3E3E3',
                                                  'TEXT_INPUT': 'black',
                                                  'BUTTON': ('white', '#6D9F85'),
                                                  'PROGRESS': 'white',
                                                  'BORDER': 1,
                                                  'SLIDER_DEPTH': 0,
                                                  'PROGRESS_DEPTH': 0}

        sg.LOOK_AND_FEEL_TABLE['HDV'] = {'BACKGROUND': '#2c2e25',
                                                  'TEXT': '#a3a3a3',
                                                  'INPUT': '#676866',
                                                  'SCROLL': '#E3E3E3',
                                                  'TEXT_INPUT': '#eec606',
                                                  'BUTTON': ('black', '#bcd800'),
                                                  'PROGRESS': '#bcd800',
                                                  'BORDER': 1,
                                                  'SLIDER_DEPTH': 0,
                                                  'PROGRESS_DEPTH': 0}
        sg.set_options(suppress_raise_key_errors=True)
        sg.theme('HDV')
    
    def initilisation(self, action, pause = 0):
        ag.PAUSE = pause
        self.packetRead = action
        self.load()

    def load(self):
        if self.stopSniff is None:
            flushBuffers()
            self.stopSniff = self.startSniff(self.packetRead)
            print(Fore.GREEN + "Module started !" + Fore.RESET)
            try:
                self._moduleWindow['ON/OFF'].update(image_filename=imgList['on'])
            except:
                pass
        else:
            self.stop(toggle = True) 

    def stop(self, toggle = False):
        if self.stopSniff is not None:
            self.stopSniff()
            self.stopSniff = None
            print(Fore.YELLOW + "Module stopped" + Fore.RESET)
            try:
                if toggle:
                    self._moduleWindow['ON/OFF'].update(image_filename=imgList['off'])
            except TclError:
                pass
            
    def startUi(self): 
        t = threading.Thread(target=self.buildUi, name="GUI")
        t.start()

    def closeModuleWindow(self):
        self._moduleWindow.close()
        self.buildUi()

    def buildUi(self):
        global imgList, application_path

        def fileName(file) -> str:
            pointInd = file.find('.')
            return file[:pointInd]

        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the PyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app 
            # path into variable _MEIPASS'.
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))

        

        imgFolder = application_path + '\\..\\sources\\img\\GUI'

        imgList = {fileName(str(f)): imgFolder + '\\' +
                   f for f in os.listdir(imgFolder) if '.png' in f}

        firstColumn = [
                    [sg.Radio("Treasure Hunt Bot", default = True, group_id = "CHOICE", key = 'huntBot')],
                    [sg.Radio("Treasure Hunt Helper", group_id = "CHOICE", key = 'huntHelper')],
                    [sg.Radio("HDV Items Listing", group_id = "CHOICE", key = 'hdv')],
                    [sg.Radio("HDV Missing Items", group_id = "CHOICE", key = 'hdvMissing')],
                    [sg.Radio("No man's land", group_id = "CHOICE", key = 'nomansland')]
        ]
        
        secondColumn = [
                    [sg.Radio("Chat Searcher", group_id = "CHOICE", key = 'chat')],
                    [sg.Radio("Multicompte Tool", group_id = "CHOICE", key = 'multi')],
                    [sg.Radio("AvA Counter", group_id = "CHOICE", key = 'ava')],
                    [sg.Radio("Ressources Price Listing", group_id = "CHOICE", key = 'priceListing')],
                    [sg.Radio("Price Computer", group_id = "CHOICE", key = 'priceCompute')]
        ]

        menuLayout =[
                    [sg.Column(firstColumn),
                    sg.Column(secondColumn)],
                    [sg.Button("Launch", key = "LAUNCH", use_ttk_buttons = True)]
            ]

        menuWindow = sg.Window(
            title = "DHM",
            layout = menuLayout,
            margins = (20, 5),
            border_depth=3,
            keep_on_top=False,
            finalize=True,
            element_justification= 'center',
            icon = application_path + '\\..\\sources\\img\\icon\\phoenix.ico',
            use_default_focus = False
            )

        while True:
            event, values = menuWindow.read()
            if event == "LAUNCH":
                for key in values:
                    if values[key]:
                        self.userChoice = key
                        self.botting = values['huntBot']
                        break
                break
            elif (event == sg.WIN_CLOSED):
                self.userChoice = "quit"
                break
        menuWindow.close()
        try:
            if (self.userChoice == 'huntHelper') or (self.userChoice == 'huntBot'):
                self.startTreasureHuntUi()
            elif (self.userChoice == 'hdv'):
                self.startHdvUi()
            elif (self.userChoice == 'chat'):
                self.startSearcherUi()
            elif (self.userChoice == 'multi'):
                self.startMulticompteUi()
            elif (self.userChoice == 'ava'):
                from modules.avaCounter import packetRead
                self.initilisation(packetRead, 0)
            elif (self.userChoice == 'hdvMissing'):
                self.startMissingItemsUi()
            elif (self.userChoice == 'priceListing'):
                self.startPriceListingUi()
            elif (self.userChoice == 'priceCompute'):
                self.startPriceComputerUi()
            elif (self.userChoice == 'nomansland'):
                self.startNomansland()
        except AttributeError:
            return

    def startTreasureHuntUi(self):

        from modules.treasureHuntBot import TreasureHuntHelper
        self.initilisation(TreasureHuntHelper(self.botting).packetRead, 0)

        sg.theme('TreasureHunt')

        botLayout = [
            [
                sg.Button(image_filename=imgList['on'], button_color=(sg.theme_background_color(
                ), sg.theme_background_color()), border_width=0, key="ON/OFF", pad=(10, 0)),
                sg.Button(image_filename=imgList['exit'], button_color=(sg.theme_background_color(
                ), sg.theme_background_color()), border_width=0, key='EXIT', image_size=(30, 30))
            ],
            [sg.Text("Position info", key="INFO",
                     font=('Helvetica', 15, 'bold'))],
            [sg.HorizontalSeparator()],
            [sg.Image(filename=imgList['noDirection'], key="DIRECTION")],
            [sg.Button(image_filename=imgList['placeHolder'], button_color=(
                sg.theme_background_color(), sg.theme_background_color()), border_width=0, key="IMAGE")]
        ]

        self._moduleWindow = sg.Window(
            title="Treasure Hunt Helper",
            no_titlebar=True,
            grab_anywhere=True,
            layout=botLayout,
            margins=(0, 0),
            border_depth=3,
            keep_on_top=True,
            finalize=True,
            alpha_channel=.85,
            element_justification = CENTER)

        while True:
            event, values = self._moduleWindow.read(timeout=15000)
            if event == "IMAGE":
                if self.found is not None:
                    self.clickNextStep()
            elif event == "ON/OFF":
                self.load()
            elif (event == sg.WIN_CLOSED) or (event == "EXIT"):
                self.stop(toggle = True)
                break
            self._moduleWindow.refresh()

        sg.theme('HDV')
        self.closeModuleWindow()

    def startHdvUi(self):
        from modules.hdvListing import packetRead

        # self.initilisation(packetRead, 0.3)

        layout = [
            [sg.Text("Waiting for a tab click", key = "INFO", size = (30, 1))],
            [sg.Button(image_filename=imgList['off'], button_color=('#2c2e25','#2c2e25'), border_width=0, key="ON/OFF", pad=(10, 0))]
        ]
        sg.theme('HDV')
        self._moduleWindow = sg.Window(
            'Données ventes', 
            layout, 
            resizable = True, 
            element_justification = 'center', 
            grab_anywhere = True,
            size=(290, 75),
            keep_on_top=True,
            )

        loaded = False
        while True:
            event, values = self._moduleWindow.read()
            if event == sg.WIN_CLOSED:
                self.stop(toggle = True)
                break
            elif event == "ON/OFF":
                if not loaded:
                    self.initilisation(packetRead, 0.3)
                    loaded = True
                else:
                    self.load()
        self.closeModuleWindow()

    def startPriceListingUi(self):
        from modules.pricesListing import PriceListing

        packetRead = PriceListing().packetRead

        layout = [
            [sg.Text("Item index", key = "INFO", auto_size_text="true")],
            [sg.Button(image_filename=imgList['off'], button_color=('#2c2e25','#2c2e25'), border_width=0, key="ON/OFF", pad=(10, 0))]
        ]

        sg.theme('HDV')
        self._moduleWindow = sg.Window(
            'Ressources Price Listing', 
            layout, 
            resizable = True, 
            element_justification = 'center', 
            grab_anywhere = True,
            keep_on_top=True,
            )

        loaded = False
        while True:
            event, values = self._moduleWindow.read()
            if event == sg.WIN_CLOSED:
                self.stop(toggle = True)
                break
            elif event == "ON/OFF":
                if not loaded:
                    self.initilisation(packetRead, 0.3)
                    loaded = True
                else:
                    self.load()
        self.closeModuleWindow()

    def startPriceComputerUi(self):
        from modules.priceCompute import PriceComputer

        packetRead = PriceComputer().packetRead
        self.initilisation(packetRead, 0.3)

        layout = [
            [sg.Text("Item Price", key = "INFO", size = (15, 1), text_color = "#ffea00", font = ('Helvetica', 30))],
            [sg.Button(image_filename=imgList['off'], button_color=('#2c2e25','#2c2e25'), border_width=0, key="ON/OFF", pad=(10, 0), visible= False)]
        ]

        sg.theme('HDV')
        self._moduleWindow = sg.Window(
            'Ressources Price Listing', 
            layout, 
            no_titlebar=True,
            resizable = True, 
            element_justification = 'center', 
            grab_anywhere = True,
            keep_on_top=True,
            size = (250, 70)
            )

        while True:
            event, values = self._moduleWindow.read()
            if event == sg.WIN_CLOSED:
                self.stop(toggle = True)
                break
            elif event == "ON/OFF":
                self.load()
        self.closeModuleWindow()
        
    def startSearcherUi(self):
        from modules.stringSearch import Searcher
        sg.theme = 'HDV'
        layout = [
            [sg.Multiline(size = (50, 5),
            key = '-INPUT-', 
            background_color= '#696968', 
            text_color = '#eec606', 
            font = 'Lato')],
            [sg.Button(image_filename=imgList['off'], button_color=('#2c2e25',
            '#2c2e25'), border_width=0, key="ON/OFF", pad=(10, 0))]
        ]

        self._moduleWindow = sg.Window('Chat Searcher', layout, finalize = True, element_justification= 'center')

        loaded = False
        searcher = Searcher()
        while True:
            event, values = self._moduleWindow.read()

            if event == sg.WIN_CLOSED:
                self.stop(toggle = True)
                break
            elif event == 'ON/OFF':
                if not loaded:
                    self.initilisation(searcher.packetRead, 0)
                    loaded = True
                else:
                    self.load()
                searcher.update(values['-INPUT-'])
        self.closeModuleWindow()

    def startNomansland(self):
        from modules.nomanslandSniffer import Nomansland
        sg.theme = 'HDV'
        layout = [
            [sg.Button(image_filename=imgList['off'], button_color=('#2c2e25',
            '#2c2e25'), border_width=0, key="ON/OFF", pad=(10, 0))]
        ]

        self._moduleWindow = sg.Window('Autopilotage Searcher', layout, finalize = True, element_justification= 'center')

        loaded = False
        searcher = Nomansland()
        while True:
            event, values = self._moduleWindow.read()

            if event == sg.WIN_CLOSED:
                self.stop(toggle = True)
                break
            elif event == 'ON/OFF':
                if not loaded:
                    self.initilisation(searcher.packetRead, 0)
                    loaded = True
                else:
                    self.load()
        self.closeModuleWindow()

    def startMulticompteUi(self):
        from modules.multicompte import Multicompte

        def rowElement(ind):
            return [[sg.In('', k = 'I' + f'{ind}', size =(15, 0)), sg.Checkbox('Mule', k = 'CB' + f'{ind}')]] 

        layout = [[sg.Column(rowElement(i), visible = False, k = 'ROW' + f'{i}')] for i in range(8)]
        layout += [[sg.Button('Add character', key = '-ADD-'), sg.Button('Save config', key = '-SAVE-')]]
        layout += [[sg.Button(image_filename=imgList['off'], button_color=('#2c2e25',
            '#2c2e25'), border_width=0, key="ON/OFF", pad=(10, 0))]]
        self._moduleWindow = sg.Window('Multicompte Tool', layout, element_justification = 'center')

        characterInd = 0
        loaded = False

        while True:
            event, values = self._moduleWindow.read()

            if event == sg.WIN_CLOSED:
                self.stop()
                break
            elif (event == '-ADD-') and (characterInd < 8):
                self._moduleWindow['ROW' + str(characterInd)].update(visible = True)
                characterInd += 1
            elif event == 'ON/OFF':
                manager = Multicompte(values)
                if not loaded:
                    self.initilisation(manager.packetRead, 0)
                    loaded = True
                else:
                    self.load()
            elif event == '-SAVE-':
                characters = []
                for i in range(8):
                    if values['I' + str(i)] != '':
                        characters.append({
                            "name": values['I' + str(i)],
                            "mule": values['CB' + str(i)]
                        })
                    else:
                        break
                from json import dump
                with open('config/multicompte.json', 'w') as outFile:
                    dump(characters, outFile)
        self.closeModuleWindow()

    def startMissingItemsUi(self):
        from modules.hdvMissingItems import MissingItemLookup
        missingItems = MissingItemLookup(self)
        if self._abortWindow:
            return
        self.initilisation(missingItems.packetRead, 0)


        sg.theme = 'HDV'
        layout = [
            [sg.Button(button_text="Save", border_width=0, key="save", pad=(10, 0))]
        ]

        self._moduleWindow = sg.Window(
            'Missing Items Excel', 
            layout, 
            finalize = True, 
            element_justification= 'center',
            grab_anywhere=True,
            keep_on_top=True,
            use_default_focus = False
            )

        while True:
            event, values = self._moduleWindow.read()

            if event == sg.WIN_CLOSED:
                self.stop()
                break
            elif event == "save":
                missingItems.saveMissingItems()
                self.stop()
                break

        self.closeModuleWindow()


    def dataUpdate(self, data, colors = None):
        self._moduleWindow['-TABLE-'].update(values = data, row_colors = colors)
        self._moduleWindow.bring_to_front()
        self._moduleWindow['-BAR-'].update(current_count = 100, visible = False)
        # self._moduleWindow['-BAR-'].update_bar(0)
        self._moduleWindow['-PERCENT-'].update(visible  = True, disabled = False)
        self._moduleWindow['-AUTOMATE-'].update(visible = True)
        self.load()

    def updateProgressBar(self, value):
        self._moduleWindow['-BAR-'].update_bar(value)

    def changeImg(self, imgName):
        if (imgName == "found") or (imgName == "checkpoint") or (imgName == "combat"):
            self.found = imgName
        try:
            self._moduleWindow["IMAGE"].update(image_filename=imgList[imgName])
        except KeyError:
            self._moduleWindow["IMAGE"].update(image_filename=imgList['tooFar'])

    def changeText(self, info):
        self._moduleWindow["INFO"].update(info)

    def changeDirection(self, dir="noDirection"):
        self._moduleWindow["DIRECTION"].update(filename=imgList[dir])

    def clickNextStep(self):
        currentX, currentY = ag.position()
        try:
            if self.found == "found":
                pos = ag.locateCenterOnScreen(application_path + '\\..\\sources\\img\\pixel\\' + 'flag.png', grayscale=True, confidence=.8)
                ag.leftClick(pos[0], pos[1])
            elif self.found == "checkpoint":
                pos = ag.locateCenterOnScreen(application_path + '\\..\\sources\\img\\pixel\\' + 'checkpoint.png', grayscale=True, confidence=.8)
                ag.leftClick(pos[0], pos[1])
            elif self.found == "combat":
                pos = ag.locateCenterOnScreen(application_path + '\\..\\sources\\img\\pixel\\' + 'combat.png', grayscale=True, confidence=.8)
                ag.leftClick(pos[0], pos[1])
        except TypeError:
            print("No next step detected, need to do it manually")

        ag.moveTo(currentX, currentY)
        self.found = None
    
    def warningPopup(self):
        sg.Popup('WARNING', 'L\'item va être posté à un prix très éloigné du prix moyen estimé. Etes-vous sûr de vouloir le poster à ce prix ?')

    def overWrite(self):
        layout = [
            [sg.Text("Today's items were already loaded. Do you want to overwrite them ?")],
            [sg.Button("Yes", key = "yes"), sg.Button("No", key = "no")]
        ] 

        window = sg.Window(
            'Overwrite warning', 
            layout,
            use_default_focus=False,
            keep_on_top=True,
            no_titlebar=True,
            element_justification='center',
            grab_anywhere=False,
            )

        event, values = window.read()
        if event == "yes":
            window.close()
            return True
        else:
            window.close()
            return False

    def abortWindow(self):
        self._abortWindow = True
        
def init(startSniff):
    global ui
    ui = GraphicalInterface(startSniff)
    try:
        ui.startUi()
    except sg.FailSafeException:
        print(Fore.RED + 'Fail Safe Activated, aborting' + Fore.RESET)

