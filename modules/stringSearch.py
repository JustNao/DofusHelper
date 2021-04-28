print('Importing sources ...')
from sniffer import protocol
from colorama import Fore

print('Sources imported !')

class Searcher:
    def __init__(self, needle = '') -> None:
        self.update(needle)

    def packetRead(self, msg):
        if msg.id == 202:
            packet = protocol.read(protocol.msg_from_id[msg.id]["name"], msg.data)
            found = any(str.lower() in packet['content'].lower() for str in self.needle)
            if found:
                print(Fore.LIGHTBLUE_EX + packet['senderName'] + Fore.RESET, ':', packet['content'])

    def update(self, string):
        needle = string.strip('\n')
        needle = needle.split(';')
        self.needle = needle