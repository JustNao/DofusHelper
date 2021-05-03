print('Importing sources ...')
from PIL.ImageOps import grayscale
from sniffer import protocol
import requests
import time
import os, sys
from colorama import init, Fore, Style
from sources.id import mapIdToCoords, textId, poiToName, npcToName, monsterToName, archiNameList
import ui.gui as g
import pyautogui as ag
from random import random
import math
print('Sources imported !')

init()  # Don't touch, used for colors in terminal

class TreasureHuntHelper():

    def __init__(self, bot=False) -> None:
        # dict.loadIds()
        global DEBUG
        DEBUG = False
        print("Treasure helper initialized")
        self.botting = bot
        # CurrentMap, TreasureHuntMessage, TreasurePOI, TreasureHinT, MapComplementaryInformationsDataMessage, FightStart
        self.interestingPackets = [7033, 3696, 7529, 9917, 2291, 5072, 9401]
        self.playerPos = self.Position()
        self.hintPos = self.Hint()
        self.timeStart = None
        self.timeStart = 0
        self.direction = "stay"
        self.clientHintName = None
        self.checkPositions = []
        self.phorreur = {
            "lookingFor": False,
            "npcId": 2673
        }
        if self.botting:
            self.initBotting()
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the PyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app 
            # path into variable _MEIPASS'.
            self.application_path = sys._MEIPASS
        else:
            self.application_path = os.path.dirname(os.path.abspath(__file__))

    class Hint:
        def __init__(self, posX=0, posY=0, d=666):
            self.x = posX
            self.y = posY
            self.distance = d

        def __str__(self):
            return '[' + str(self.x) + ',' + str(self.y) + ']'

    class Position:
        def __init__(self, posX=0, posY=0):
            self.x = posX
            self.y = posY

        def __str__(self):
            return '[' + str(self.x) + ',' + str(self.y) + ']'

    def initBotting(self):
        # Initialisation du bot, fixe les positions de changement de carte
        ag.FAILSAFE = True
        self.sizeX, self.sizeY = ag.size()
        bottomScreen = ag.locateOnScreen(os.path.dirname(os.path.realpath(
            '__file__')) + '\\sources\\img\\pixel\\bottomScreen.png', grayscale=True, confidence=.75)
        if bottomScreen is None:
            print(
                Fore.RED + "Error : please keep your Dofus window open for the initilization. You need to restart." + Fore.RESET)
            return

        self.movePos = {
            "right": (self.sizeX - 50, self.sizeY/2),
            "left": (50, self.sizeY/2),
            "top": (self.sizeX/2, 10),
            "bottom": (bottomScreen.left, bottomScreen.top - 10)
        }

        self.WAIT_TIME = 2

    def move(self):
        # Déplacement du bot
        if (not self.botting) or (self.hintPos.distance > 10 and not self.phorreur['lookingFor']):
            return

        currentMousePos = ag.position()
        # time.sleep(random()*2) # Temps de pause entre chaque action, risqué car fait attendre le thread entier
        try:

            x, y = self.movePos[self.direction]
            ag.moveTo(x, y)

            if (self.direction == 'top') or (self.direction == 'bottom'):
                ag.PAUSE = 0.2
                time.sleep(0.2)

            while ag.locateOnScreen(os.path.dirname(os.path.realpath(
                    '__file__')) + '\\sources\\img\\pixel\\groupOnMouse.png', grayscale=True, confidence=0.75) is not None:
                x += random()*50 - 25
                ag.moveTo(x, y)

            ag.PAUSE = 0
            print("Bot moved", Fore.YELLOW + self.direction + Fore.RESET)
            ag.click()
        except KeyError:
            # print("Bot can't move, need to stay put")
            pass

        ag.moveTo(currentMousePos)

    def packetRead(self, msg):
        if msg.id in self.interestingPackets:
            try:
                packet = protocol.read(protocol.msg_from_id[msg.id]["name"], msg.data)
            except KeyError:
                print("KeyError ", msg.id)
                return
            if msg.id == 7033:  # Changement de Map
                self.changeMap(packet)
            elif msg.id == 3696:  # Nouvelle étape de chasse aux trésors
                self.huntNewStep(packet)
            elif (msg.id == 5072):  # Chargement de carte, recherche d'un phorreur
                self.mapContentAnalyse(packet)
            elif (msg.id == (4119 or 9401)):
                # En entrant en combat, on met en pause le sniffer pour éviter les problèmes
                g.ui.load()
        if DEBUG:
            print(protocol.msg_from_id[msg.id]["name"])

    def changeMap(self, packet):
        self.playerPos = self.Position(
            mapIdToCoords[packet['mapId']][0], mapIdToCoords[packet['mapId']][1])
        print("New position : ", self.playerPos.__str__())
        self.stepUpdate()

    def stepUpdate(self):
        # Actualise le modèle à chaque changement de carte #

        if (self.hintPos.distance <= 10) and (abs(self.playerPos.x - self.hintPos.x) <= 10) and (abs(self.playerPos.y - self.hintPos.y) <= 10) and (not self.phorreur['lookingFor']):
            if self.playerPos.x != self.hintPos.x:
                self.hintPos.distance = abs(self.playerPos.x - self.hintPos.x)

                if DEBUG:
                    print("Horizontal distance from hint : ", Fore.GREEN +
                      str(self.hintPos.distance) + Fore.RESET)
                
                g.ui.changeImg(str(int(self.hintPos.distance)))

                if self.playerPos.x < self.hintPos.x:
                    direction = 'right'
                else:
                    direction = 'left'

                g.ui.changeDirection(direction)
                self.direction = direction

            elif self.playerPos.y != self.hintPos.y:
                self.hintPos.distance = abs(self.playerPos.y - self.hintPos.y)
                
                if DEBUG:
                    print("Vertical distance from hint : ", Fore.GREEN +
                      str(self.hintPos.distance) + Fore.RESET)

                g.ui.changeImg(str(int(self.hintPos.distance)))

                if self.playerPos.y < self.hintPos.y:
                    direction = 'bottom'
                else:
                    direction = 'top'

                g.ui.changeDirection(direction)
                self.direction = direction

            else:
                print(Fore.GREEN + "Hint found !" + Fore.RESET)
                g.ui.changeImg("found")
                g.ui.changeDirection()
                self.direction = "stay"
                time.sleep(1)
                if self.botting:
                    g.ui.clickNextStep()

    def reset(self):
        self.hintPos.distance = 666
        self.direction = "stay"
        self.phorreur['lookingFor'] = False

    def mapContentAnalyse(self, packet):
        for actor in packet["actors"]:
            if (actor['__type__'] == "GameRolePlayTreasureHintInformations"):
                if (actor['npcId'] == self.phorreur['npcId'] and (self.phorreur['lookingFor'] == True)):
                    print(Fore.GREEN + "Phorreur found !" + Fore.RESET)
                    self.phorreur['lookingFor'] = False
                    self.hintPos = self.Hint(
                        self.playerPos.x, self.playerPos.y, 0)

                    g.ui.changeImg('found')
                    self.direction = "stay"
                    g.ui.changeDirection()
                    if self.botting:
                        g.ui.clickNextStep()

                    break
            elif (actor['__type__'] == 'GameRolePlayGroupMonsterInformations'):
                mainMob = actor['staticInfos']['mainCreatureLightInfos']['genericId']
                if monsterToName(mainMob) in archiNameList:
                    print(Fore.BLUE + "Archimonstre found !" + Fore.RESET)
                    g.ui.changeImg('archimonstre')
                    g.ui.load()
                    self.direction = "stay"
                    break


        self.move()

    def huntNewStep(self, packet):
        self.reset()
        starting = False
        if len(packet['flags']) == 0:
            self.checkPositions.clear()
            self.checkPositions.append(
                (mapIdToCoords[packet['startMapId']][0], mapIdToCoords[packet['startMapId']][1]))
            if (packet['checkPointCurrent'] == 0):
                print(Fore.YELLOW + "Starting treasure hunt" + Fore.RESET)
                self.timeStart = time.time()
                self.playerPos = self.Position(-25, -36)  # Malle aux trésors
                g.ui.changeDirection()
                starting = True
                # ag.click(ag.locateCenterOnScreen(os.path.dirname(os.path.realpath(
                    # '__file__')) + '\\sources\\img\\pixel\\sideBlack.png', grayscale = True, confidence = 0.75))
        elif len(packet['flags']) == packet['totalStepCount']:
            g.ui.changeImg("checkpoint")
            print(Fore.YELLOW + "Checkpoint reached !" + Fore.RESET)
            if self.botting:
                g.ui.clickNextStep()
            g.ui.changeDirection()
            return

        if packet['checkPointCurrent'] >= packet['checkPointTotal'] - 1:
            end = time.time()
            print(Fore.MAGENTA + "Treasure found !" + Fore.RESET)
            print("This hunt took ", Fore.CYAN + str(int(end -
                                                         self.timeStart)) + Fore.RESET, " seconds to finish")
            g.ui.changeImg('combat')
            g.ui.load()
            return

        intDirection = packet['knownStepsList'][-1]['direction']
        if intDirection == 0:
            strDirection = 'right'
        elif intDirection == 2:
            strDirection = 'bottom'
        elif intDirection == 4:
            strDirection = 'left'
        else:
            strDirection = 'top'
        
        if not starting:
            self.direction = strDirection

        if packet['knownStepsList'][-1]['__type__'] == 'TreasureHuntStepFollowDirectionToPOI':
            # Using Dofus-Map API to get hints based on position and direction
            if (len(packet['flags']) == 0):
                lastCheckPoint = packet['startMapId']
            else:
                lastCheckPoint = packet['flags'][-1]['mapId']

            url = 'https://dofus-map.com/huntTool/getData.php?x=' + str(mapIdToCoords[lastCheckPoint][0]) + '&y=' + str(
                mapIdToCoords[lastCheckPoint][1]) + '&direction=' + strDirection + '&world=0&language=fr'
            get = requests.get(url)
            js = get.json()

            clientHintName = poiToName(
                packet['knownStepsList'][-1]['poiLabelId'])

            for hint in js['hints']:
                dofusMapName = textId[str(hint['n'])]
                if clientHintName == dofusMapName:
                    if (hint['d'] < self.hintPos.distance) and ((hint['x'], hint['y']) not in self.checkPositions):
                        self.hintPos = self.Hint(
                            hint['x'], hint['y'], hint['d'])

            if self.hintPos.distance == 666:
                print(Fore.RED + "ERROR : no hint found !" + Fore.RESET)
                print(packet)
                g.ui.changeText("No hint found")
                g.ui.changeImg('found')
                self.direction = "stay"
            else:
                self.checkPositions.append((self.hintPos.x, self.hintPos.y))
                print(Fore.YELLOW + clientHintName + Fore.RESET + " found " + Fore.GREEN + str(self.hintPos.distance) + Fore.RESET +
                      " maps " + Fore.GREEN + strDirection + Fore.RESET + " at " + Fore.YELLOW + self.hintPos.__str__() + Fore.RESET)
                g.ui.changeText(self.hintPos.__str__())
                g.ui.changeDirection(strDirection)
                g.ui.changeImg(str(int(math.sqrt(math.pow(
                    self.playerPos.y - self.hintPos.y, 2) + math.pow(self.playerPos.x - self.hintPos.x, 2)))))
                self.stepUpdate()
                self.move()

        else:
            clientHintName = npcToName(packet['knownStepsList'][-1]['npcId'])
            print(Fore.YELLOW + "Phorreur" + Fore.RESET + " to find ", Fore.GREEN +
                  strDirection + Fore.RESET)
            self.phorreur['lookingFor'] = True
            self.phorreur['npcId'] = packet['knownStepsList'][-1]['npcId']
            g.ui.changeDirection(strDirection)
            g.ui.changeImg("phorreur")

            if (len(packet['flags']) == 0) and (packet['checkPointCurrent'] == 0):
                # Si un phorreur est détécté en tout premier, il ne faut pas commencer à le chercher
                self.direction = "stay"

            self.move()
