print('Importing sources ...')
from sniffer import protocol
from .pricesListing import kamasToString, craftPrice
from colorama import Fore
from ui.gui import ui
print('Sources imported !')

class PriceComputer:
    def packetRead(self, msg):
        # print(msg.id, protocol.msg_from_id[msg.id]['name'], sep = ', ')
        if msg.id == 1313:
            # 1313, ExchangeStartedSellerMessage
            packet = protocol.readMsg(msg)
            if packet is None:
                return
            if packet['channel'] == 4:
                # group channel
                if packet['content'][0] == '$':
                    args = packet['content'].split()
                    if args[0][1:] == 'price':
                        price = craftPrice(packet['objects'][0]['objectGID'])
                        if price != 0:
                            ui.changeText(kamasToString(price) + " K")
                        else:
                            ui.changeText("Missing an item")
