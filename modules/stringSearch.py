from playsound import playsound
from sniffer import protocol
from colorama import Fore
import os


class Searcher:
    def __init__(self, needle='') -> None:
        self.update(needle)

    def packetRead(self, msg):
        name = protocol.msg_from_id[msg.id]["name"]
        if name == "ChatServerMessage":
            packet = protocol.read(name, msg.data)
            found = any(
                str.lower() in packet['content'].lower() for str in self.needle)
            if found:
                path = os.path.abspath(
                    os.path.join(os.getcwd(), 'sources/sound/msg.mp3'))
                playsound(path)
                print(Fore.LIGHTBLUE_EX +
                      packet['senderName'] + Fore.RESET, ':', packet['content'])

    def update(self, string):
        needle = string.strip('\n')
        needle = needle.split(';')
        self.needle = needle
