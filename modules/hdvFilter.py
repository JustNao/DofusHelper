import re
import json
from ui.gui import ui
from colorama import Fore
from sources.effects import effects, idToEffect
from sources.item import items
from sniffer import protocol
from .pricesListing import kamasToString
import threading
import keyboard
import os
print('Importing sources ...')
print('Sources imported !')


class HDVFilter:
    # HDV Equipement Filter

    def __init__(self) -> None:
        self.item = None
        self.bids = []
        self.releventBids = []
        self.filter = {
            "118": {
                "value": 50,
                "diff": 2,
            },
        }
        self.position = 0
        keyboard.on_press_key('right', self.nextBid)
        keyboard.on_press_key('left', self.previousBid)

    def reset(self):
        self.item = None
        self.bids = []
        self.releventBids = []

    def nextBid(self, _):
        if len(self.releventBids) > 0:
            self.position = (self.position + 1) % len(self.releventBids)
            self.displayBid(self.position)

    def previousBid(self, _):
        if len(self.releventBids) > 0:
            self.position = (self.position - 1) % len(self.releventBids)
            self.displayBid(self.position)

    def displayBid(self, index):
        os.system('CLS')

        if len(self.releventBids) == 0:
            print("No bid was found with the filter")
            return

        bid = self.releventBids[index]

        print("Bid #" + str(index + 1) + " / " +
              str(len(self.releventBids)) + " :" + Fore.YELLOW + f" {kamasToString(bid['prices'][0])} K" + Fore.RESET)
        for effectId, effect in self.item['effects'].items():
            found = False
            for bidEffect in bid['effects']:
                if bidEffect['actionId'] == effectId:
                    found = True
                    try:
                        operator = '-' if effect['operator'] == '-' else ' '
                        overCharac = bidEffect["value"] - effect['max']
                        value = bidEffect[
                            'value'] if overCharac <= 0 or effect['max'] == 0 else f"{bidEffect['value']} {Fore.CYAN}(+{overCharac}){Fore.RESET}"
                        if operator == '-':
                            print(
                                f"{operator} {Fore.RED} {value} {Fore.RED}{effect['type']}{Fore.RESET} [{effect['min']} à {effect['max']}]")
                        else:
                            print(
                                f"{operator} {Fore.GREEN} {value} {Fore.GREEN}{effect['type']}{Fore.RESET} [{effect['min']} à {effect['max']}]")
                    except KeyError:
                        print(
                            f"  {bidEffect['min']} à {bidEffect['min']} {effect['type']}")
                    break
            if not found:
                print(f"{Fore.LIGHTBLACK_EX} 0 {effect['type']}{Fore.RESET} [{effect['min']} à {effect['max']}]")
        pass

    def filterBids(self, filt):
        self.releventBids = []

        characFilter = {}
        for i in range(int(len(filt.keys())/2)):
            if filt[f'I-{i}'] != '':
                characFilter[int(filt[f'HIDDEN-{i}'])] = {
                    'value': int(filt[f'I-{i}']),
                    'diff': 0,
                }

        for bid in self.bids:
            valid = True
            for effect in characFilter:
                if not valid:
                    break
                found = False
                for packetEffect in bid['effects']:
                    if packetEffect['actionId'] == effect:
                        found = True
                        if packetEffect['value'] < (characFilter[effect]['value'] - characFilter[effect]['diff']):
                            valid = False
                            break
                if not found:
                    valid = False
            if valid:
                self.releventBids.append(bid)

        self.releventBids.sort(key=lambda x: x['prices'][0])
        self.displayBid(0)

    def packetRead(self, msg):
        name = protocol.msg_from_id[msg.id]["name"]
        if name == "ExchangeTypesItemsExchangerDescriptionForUserMessage":
            packet = protocol.readMsg(msg)
            os.system('CLS')
            if packet is None:
                return

            self.reset()
            self.item = items[packet['objectGID']]
            for bid in packet['itemTypeDescriptions']:
                self.bids.append(bid)
            print("Found", len(self.bids), "bids for", self.item['name'])

            self.item['effects'] = {}
            for effect in self.item['possibleEffects']:

                fullEffect = idToEffect[effect['effectId']]['description']
                displayEffectRaw = re.split(r'[ {}~%#]', fullEffect)
                displayEffect = []
                for split in displayEffectRaw:
                    if len(split) > 2 or split in ('PA', 'PM'):
                        displayEffect.append(split)
                if '%' in fullEffect:
                    displayEffect.append('(%)')
                elif 'Résistance' in fullEffect:
                    displayEffect.append('(Fixe)')

                operator = effects(effect['effectId'])['operator']
                self.item['effects'][effect['effectId']] = {
                    'min': effect['diceNum'],
                    'max': effect['diceSide'],
                    'type': ' '.join(map(str, displayEffect)),
                    'operator': operator,
                }

            ui.updateItem(self.item)
