from tkinter import TclError
from tkinter.constants import CENTER, DISABLED, RIGHT, LEFT
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
    
    def initilisation(self, action, pause = 0):
        ag.PAUSE = pause
        self.packetRead = action
        self.load()

    def load(self):
        if self.stopSniff is None:
            self.stopSniff = self.startSniff(self.packetRead)
            print(Fore.GREEN + "Module started !" + Fore.RESET)
            try:
                moduleWindow['ON/OFF'].update(image_filename=imgList['on'])
            except NameError:
                pass
        else:
            self.stop() 

    def stop(self):
        if self.stopSniff is not None:
            self.stopSniff()
            self.stopSniff = None
            print(Fore.YELLOW + "Module stopped" + Fore.RESET)
            try:
                moduleWindow['ON/OFF'].update(image_filename=imgList['off'])
            except NameError or TclError:
                pass 
            
    def startUi(self):
        t = threading.Thread(target=self.buildUi, name="GUI")
        t.start()

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

        # MENU #
        sg.theme('HDV')

        firstColumn = [
                    [sg.Radio("Treasure Hunt Bot", default = True, group_id = "CHOICE", key = 'huntBot')],
                    [sg.Radio("Treasure Hunt Helper", group_id = "CHOICE", key = 'huntHelper')],
                    [sg.Radio("HDV Items Listing", group_id = "CHOICE", key = 'hdv')]
        ]
        
        secondColumn = [
                    [sg.Radio("Chat Searcher", group_id = "CHOICE", key = 'chat')],
                    [sg.Radio("Multicompte Tool", group_id = "CHOICE", key = 'multi')],
                    [sg.Radio("AvA Counter", group_id = "CHOICE", key = 'ava')]
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
        except AttributeError:
            return

    def startTreasureHuntUi(self):
        global moduleWindow

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
            [sg.Text("Position info", key="POS",
                     font=('Helvetica', 15, 'bold'))],
            [sg.HorizontalSeparator()],
            [sg.Image(filename=imgList['noDirection'], key="DIRECTION")],
            [sg.Button(image_filename=imgList['placeHolder'], button_color=(
                sg.theme_background_color(), sg.theme_background_color()), border_width=0, key="IMAGE")]
        ]

        moduleWindow = sg.Window(
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
            event, values = moduleWindow.read(timeout=15000)
            if event == "IMAGE":
                if self.found is not None:
                    self.clickNextStep()
            elif event == "ON/OFF":
                self.load()
            elif (event == sg.WIN_CLOSED) or (event == "EXIT"):
                self.stop()
                break
            moduleWindow.refresh()

        moduleWindow.close()

    def startHdvUi(self):
        global moduleWindow
        from modules.hdvListing import automatePrices, packetRead

        self.initilisation(packetRead, 0.3)

        headings = ['            ITEM            ', '(1) PRIX JOUEUR', '(1) PRIX HDV', '(10) PRIX JOUEUR', '(10) PRIX HDV', '(100) PRIX JOUEUR', '(100) PRIX HDV', 'DIFFERENCE']

        layout = [
            [sg.Button(image_filename=imgList['on'], button_color=('#2c2e25',
            '#2c2e25'), border_width=0, key="ON/OFF", pad=(10, 0)),
            sg.Input('0', disabled = True, visible = False, key = '-PERCENT-', background_color = '#6e6f6e', size = (10, 10), text_color = '#eec606'),
            sg.Button('Automate Prices', visible = False, border_width = 0, key = '-AUTOMATE-'),
            sg.ProgressBar(100, key = '-BAR-', orientation = 'h', size = (20, 20), bar_color = ('#bfe700', '#6e6f6e'))],
            [sg.Table(values = [['' for _ in range(len(headings))]],
            headings = headings, 
            hide_vertical_scroll = True,
            justification = 'center',
            font = 'Lato',
            background_color = '#393a32',
            text_color = 'black',
            num_rows = 20,
            header_background_color = '#696968',
            header_text_color = '#eec606',
            key = '-TABLE-')]
        ]
        sg.theme('HDV')
        moduleWindow = sg.Window('Données ventes', layout, resizable = True, element_justification = 'center')

        while True:
            event, values = moduleWindow.read()
            if event == sg.WIN_CLOSED:
                self.stop()
                break
            elif event == "ON/OFF":
                self.load()
            elif event == "-AUTOMATE-":
                moduleWindow['-BAR-'].update(current_count = 0, visible = True)
                moduleWindow['-PERCENT-'].update(visible  = False, disabled = True)
                moduleWindow['-AUTOMATE-'].update(visible = False)
                t = threading.Thread(target=automatePrices, args = (int(float(values['-PERCENT-'])), ), name="Pricing")
                t.start()
        moduleWindow.close()
        
    def startSearcherUi(self):
        global moduleWindow
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

        moduleWindow = sg.Window('Chat Searcher', layout, finalize = True, element_justification= 'center')

        loaded = False
        searcher = Searcher()
        while True:
            event, values = moduleWindow.read()

            if event == sg.WIN_CLOSED:
                self.stop()
                break
            elif event == 'ON/OFF':
                if not loaded:
                    self.initilisation(searcher.packetRead, 0)
                    loaded = True
                else:
                    self.load()
                searcher.update(values['-INPUT-'])

    def startMulticompteUi(self):
        global moduleWindow
        from modules.multicompte import Multicompte

        def rowElement(ind):
            return [[sg.In('', k = 'I' + f'{ind}', size =(15, 0)), sg.Checkbox('Mule', k = 'CB' + f'{ind}')]] 

        layout = [[sg.Column(rowElement(i), visible = False, k = 'ROW' + f'{i}')] for i in range(8)]
        layout += [[sg.Button('Add character', key = '-ADD-')]]
        layout += [[sg.Button(image_filename=imgList['off'], button_color=('#2c2e25',
            '#2c2e25'), border_width=0, key="ON/OFF", pad=(10, 0))]]
        moduleWindow = sg.Window('Multicompte Tool', layout, element_justification = 'center')

        characterInd = 0
        loaded = False

        while True:
            event, values = moduleWindow.read()

            if event == sg.WIN_CLOSED:
                self.stop()
                break
            elif (event == '-ADD-') and (characterInd < 8):
                moduleWindow['ROW' + str(characterInd)].update(visible = True)
                characterInd += 1
            elif event == 'ON/OFF':
                manager = Multicompte(values)
                if not loaded:
                    self.initilisation(manager.packetRead, 0)
                    loaded = True
                else:
                    self.load()


    def dataUpdate(self, data, colors = None):
        moduleWindow['-TABLE-'].update(values = data, row_colors = colors)
        moduleWindow.bring_to_front()
        moduleWindow['-BAR-'].update(current_count = 100, visible = False)
        # moduleWindow['-BAR-'].update_bar(0)
        moduleWindow['-PERCENT-'].update(visible  = True, disabled = False)
        moduleWindow['-AUTOMATE-'].update(visible = True)
        self.load()

    def updateProgressBar(self, value):
        moduleWindow['-BAR-'].update_bar(value)

    def changeImg(self, imgName):
        if (imgName == "found") or (imgName == "checkpoint") or (imgName == "combat"):
            self.found = imgName
        try:
            moduleWindow["IMAGE"].update(image_filename=imgList[imgName])
        except KeyError:
            moduleWindow["IMAGE"].update(image_filename=imgList['tooFar'])

    def changeText(self, pos):
        moduleWindow["POS"].update(pos)

    def changeDirection(self, dir="noDirection"):
        moduleWindow["DIRECTION"].update(filename=imgList[dir])

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


def init(startSniff):
    global ui
    ui = GraphicalInterface(startSniff)
    try:
        ui.startUi()
    except sg.FailSafeException:
        print(Fore.RED + 'Fail Safe Activated, aborting' + Fore.RESET)

