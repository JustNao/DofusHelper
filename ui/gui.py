from tkinter.constants import CENTER, RIGHT
import PySimpleGUI as sg
import os, sys
import threading
import pyautogui as ag
from treasureHunt.treasureHuntBot import TreasureHuntHelper

class GraphicalInterface():
    def __init__(self, startSniff):
        ag.PAUSE = 0
        self.found = None
        self.packetRead = None
        self.startSniff = startSniff
        self.stopSniff = None
        self.botting = True
    
    def botInitialisation(self):
        self.packetRead = TreasureHuntHelper(self.botting).packetRead
        self.load()

    def load(self):
        if self.stopSniff is None:
            self.stopSniff = self.startSniff(self.packetRead)
            print("Packet sniffer started")
            try:
                botWindow['ON/OFF'].update(image_filename=imgList['on'])
            except NameError:
                pass
        else:
            self.stop() 

    def stop(self):
        if self.stopSniff is not None:
            self.stopSniff()
            self.stopSniff = None
            print("Packet sniffer stopped")
            try:
                botWindow['ON/OFF'].update(image_filename=imgList['off'])
            except NameError:
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

        imgFolder = application_path + '\\..\\sources\\img\\GUI'

        imgList = {fileName(str(f)): imgFolder + '\\' +
                   f for f in os.listdir(imgFolder) if '.png' in f}

        # MENU #
        sg.theme('DarkBlue')

        menuLayout =[
                [
                    sg.Radio("Treasure Hunt Bot", default = True, group_id = "CHOICE", key = 'huntBot'),
                    sg.Radio("Treasure Hunt Helper", group_id = "CHOICE", key = 'huntHelper')
                ],
                [sg.Button("Launch", key = "LAUNCH")]
            ]

        menuWindow = sg.Window(
            title = "DHM",
            layout = menuLayout,
            margins = (20, 5),
            border_depth=3,
            keep_on_top=False,
            finalize=True,
            element_justification=CENTER,
            icon = application_path + '\\..\\sources\\img\\icon\\phoenix.ico'
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
        except AttributeError:
            return

    def startTreasureHuntUi(self):
        global botWindow
        self.botInitialisation()
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

        botWindow = sg.Window(
            title="Treasure Hunt Helper",
            no_titlebar=True,
            grab_anywhere=True,
            layout=botLayout,
            margins=(0, 0),
            border_depth=3,
            keep_on_top=True,
            finalize=True,
            alpha_channel=.85,
            element_justification=CENTER)

        while True:
            event, values = botWindow.read(timeout=15000)
            if event == "IMAGE":
                if self.found is not None:
                    self.clickNextStep()
            elif event == "ON/OFF":
                self.load()
            elif (event == sg.WIN_CLOSED) or (event == "EXIT"):
                self.stop()
                break
            botWindow.refresh()

        botWindow.close()

    def changeImg(self, imgName):
        if (imgName == "found") or (imgName == "checkpoint") or (imgName == "combat"):
            self.found = imgName
        try:
            botWindow["IMAGE"].update(image_filename=imgList[imgName])
        except KeyError:
            botWindow["IMAGE"].update(image_filename=imgList['tooFar'])

    def changeText(self, pos):
        botWindow["POS"].update(pos)

    def changeDirection(self, dir="noDirection"):
        botWindow["DIRECTION"].update(filename=imgList[dir])

    def clickNextStep(self):
        currentX, currentY = ag.position()
        while True:
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
                break
            except AttributeError:
                print("No next step detected, will try in a second")

        ag.moveTo(currentX, currentY)
        self.found = None


def init(startSniff):
    global ui
    ui = GraphicalInterface(startSniff)
    ui.startUi()
