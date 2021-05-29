print('Importing sources ...')

from typing import Type
from pywinauto.findbestmatch import find_best_match
from sniffer import protocol
from colorama import Fore
from pywinauto.findwindows import find_window
from win32 import win32gui
import win32com.client as client
import pyautogui as ag
import json
print('Sources imported !')

class Perso:
    def __init__(self, id = 0, mule = False):
        self.id = id
        self.mule = mule
        self.active = False

class Multicompte:

    def __init__(self, userChoice) -> None:
        bad_chars = ' \n'
        self.characters = {}
        if userChoice['I0'] != '':
            for i in range(8):
                if userChoice['I' + str(i)] != '':
                    self.characters[userChoice['I' + str(i)]] = Perso(mule = userChoice['CB' + str(i)])
                else:
                    break
        else:   
            try:
                with open('config/multicompte.json') as file:
                    importedChars = json.load(file)
            except FileNotFoundError:
                print("No character was manually put, and no file could be detected")
                return

            for char in importedChars:
                print("Importing", char['name'])
                self.characters[char['name']] = Perso(mule = char['mule'])

        self.top_windows = []
        win32gui.EnumWindows(self.windowEnumerationHandler, self.top_windows)

    def windowEnumerationHandler(self, hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    
    def packetRead(self, msg):
        if msg.id == 3775 : 
            # 3775 PartyUpdateLightMessage
            # 9871 GameSynchronizingMessage
            packet = protocol.readMsg(msg)
            if packet is None:
                return
            try:
                # for entity in packet['fighters']:
                #     if entity['__type__'] == 'GameFightCharacterInformations':
                #         self.characters[entity['name']].id = entity['contextualId']
                charName = win32gui.GetWindowText(win32gui.GetForegroundWindow()).split()[0]
                if (charName in self.characters.keys()) and (self.characters[charName].id == 0):
                    self.characters[charName].id = packet['id']
                    print("Setting up", charName)
            except KeyError:
                pass
        elif msg.id == 3049:
            # GameFightTurnStartMessage
            packet = protocol.readMsg(msg)
            if packet is None:
                return
            name = self.idToName(packet['id'])
            if name not in self.characters.keys() or self.characters[name].active:
                return

            for char in self.characters:
                self.characters[char].active = (char == name)
            
            shell = client.Dispatch("WScript.Shell")
            shell.SendKeys('%')
            print("Bringing up", name)
            win32gui.SetForegroundWindow(find_window(best_match = name + ' - Dofus'))
            if self.characters[name].mule:
                ag.typewrite(['v'])


    def idToName(self, id):
        for character in self.characters:
            if self.characters[character].id == id:
                return character
# Epoque, Imminent
