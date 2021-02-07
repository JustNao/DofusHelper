print('Importing sources ...')

from sniffer import protocol
from colorama import Fore
from pywinauto.findwindows import find_window
from win32 import win32gui
import win32com.client as client
print('Sources imported !')

class Multicompte:
    def __init__(self, characterList) -> None:
        bad_chars = ' \n'
        fullCharacaterList = characterList
        for c in bad_chars: 
            fullCharacaterList = fullCharacaterList.replace(c, "")
        self.charactersName = fullCharacaterList.split(',')

        self.characterId = {}
        self.top_windows = []
        win32gui.EnumWindows(self.windowEnumerationHandler, self.top_windows)

    def windowEnumerationHandler(self, hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    
    def packetRead(self, msg):
        if msg.id == 5570:
            packet = protocol.read(protocol.msg_from_id[msg.id]["name"], msg.data)
            try:
                for teamMember in packet['team']['teamMembers']:
                    self.characterId[teamMember['id']] = teamMember['name']
            except KeyError:
                pass
        elif msg.id == 9013:
            packet = protocol.read(protocol.msg_from_id[msg.id]["name"], msg.data)
            try:
                shell = client.Dispatch("WScript.Shell")
                shell.SendKeys('%')
                win32gui.SetForegroundWindow(find_window(title=self.characterId[packet['id']] + ' - Dofus 2.58.5.8'))
            except KeyError:
                pass

# Epoque, Taty-Citron
