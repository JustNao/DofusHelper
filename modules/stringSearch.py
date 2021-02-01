print('Importing sources ...')
from sniffer import protocol
from colorama import Fore

print('Sources imported !')

class Searcher:
    def __init__(self, needle = '') -> None:
        self.needle = needle.strip('\n')

    def packetRead(self, msg):
        if msg.id == 7831:
            packet = protocol.read(protocol.msg_from_id[msg.id]["name"], msg.data)
            if self.needle.lower() in packet['content'].lower():
                print(Fore.LIGHTBLUE_EX + packet['senderName'] + Fore.RESET, ':', packet['content'])

    def update(self, string):
        self.needle = string.strip('\n')