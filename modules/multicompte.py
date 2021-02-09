print('Importing sources ...')

from typing import Type
from pywinauto.findbestmatch import find_best_match
from sniffer import protocol
from colorama import Fore
from pywinauto.findwindows import find_window
from win32 import win32gui
import win32com.client as client
import pyautogui as ag
print('Sources imported !')

class Perso:
    def __init__(self, id = 0, mule = False):
        self.id = id
        self.mule = mule

class Multicompte:

    def __init__(self, userChoice) -> None:
        bad_chars = ' \n'

        self.characters = {}
        for i in range(8):
            if userChoice['I' + str(i)] != '':
                self.characters[userChoice['I' + str(i)]] = Perso(mule = userChoice['CB' + str(i)])
            else:
                break

        self.top_windows = []
        win32gui.EnumWindows(self.windowEnumerationHandler, self.top_windows)

    def windowEnumerationHandler(self, hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    
    def packetRead(self, msg):
        if msg.id == 5570:
            packet = protocol.read(protocol.msg_from_id[msg.id]["name"], msg.data)
            try:
                for teamMember in packet['team']['teamMembers']:
                    self.characters[teamMember['name']].id = teamMember['id']
            except KeyError:
                pass
        elif msg.id == 9013:
            packet = protocol.read(protocol.msg_from_id[msg.id]["name"], msg.data)
            try:
                shell = client.Dispatch("WScript.Shell")
                shell.SendKeys('%')
                name = self.idToName(packet['id'])
                win32gui.SetForegroundWindow(find_window(best_match = name + ' - Dofus'))
                if self.characters[name].mule:
                    ag.typewrite(['v'])
            except KeyError:
                pass
            except TypeError:
                pass

    def idToName(self, id):
        for character in self.characters:
            if self.characters[character].id == id:
                return character
# Epoque, Taty-Citron
