from tiles import *
from agent import *
from loadTiles import *
from random import randint
from converser import *
from tiles import *
from object import *
from action import *

class Level:
    def __init__(self, levelFile, agentFile, objectFile, actionFile, tileIdToTile):
        self.tileIdToTile = tileIdToTile

        self.lightState = ""
        self.state = ""
        self.hasObjective = False
        self.objective = ""

        self.lightingOn = True
        self.ambientLight = (255, 255, 255)

        self.torchOn = False
        #self.torchLight = (226, 244, 66)

        self.messages = []
        self.readyForNextLevel = False

        self.readFromFile(levelFile, agentFile, objectFile, actionFile)
        
    def readFromFile(self, levelFile, agentFile, objectFile, actionFile):

        # build the basic grid
        f = open(levelFile)
        lines = f.readlines()
        self.grid = []
        for line in lines:
            l = line.split(',')
            newl = []
            for i in l:
                newl.append(self.tileIdToTile[int(i)])
            self.grid.append(newl)
        
        self.width = len(self.grid[0])
        self.height = len(self.grid)


        # read in the objects
        f = open(objectFile)
        lines = f.readlines()
        self.objects = []

        for line in lines:
            objectInfo = line.split(',')
                    
            tile = self.tileIdToTile[objectInfo[OBJECT_SPRITE_INDEX]]

            dialogue = objectInfo[OBJECT_DIALOGUE_INDEX].replace("*comma*", ",")
            o = Object(objectInfo[OBJECT_NAME_INDEX], tile, dialogue)

            o.setPosition(int(objectInfo[OBJECT_X_INDEX]),
                          int(objectInfo[OBJECT_Y_INDEX]))

            self.objects.append(o)
        
        # read in the agents
        f = open(agentFile)
        lines = f.readlines()
        self.agents = []
        
        # lines[0] should contain the player
        playerInfo = lines[0].split(',')
        playerTiles = [self.tileIdToTile[playerInfo[AGENT_UP_SPRITE_INDEX]],
                       self.tileIdToTile[playerInfo[AGENT_DOWN_SPRITE_INDEX]],
                       self.tileIdToTile[playerInfo[AGENT_LEFT_SPRITE_INDEX]],
                       self.tileIdToTile[playerInfo[AGENT_RIGHT_SPRITE_INDEX]]]

        
        playerAttackTiles = [self.tileIdToTile[playerInfo[AGENT_UP_ATTACK_SPRITE_INDEX]],
         self.tileIdToTile[playerInfo[AGENT_DOWN_ATTACK_SPRITE_INDEX]],
         self.tileIdToTile[playerInfo[AGENT_LEFT_ATTACK_SPRITE_INDEX]],
         self.tileIdToTile[playerInfo[AGENT_RIGHT_ATTACK_SPRITE_INDEX]]]

        print playerTiles
        print playerAttackTiles
        
        self.player = Agent(playerInfo[AGENT_NAME_INDEX], playerTiles, playerAttackTiles)

        self.player.setPosition(int(playerInfo[AGENT_X_INDEX]),
                                int(playerInfo[AGENT_Y_INDEX]))
        self.agents.append(self.player)

        for line in lines[1:]:
            agentInfo = line.split(',')
            
            eTiles = [self.tileIdToTile[agentInfo[AGENT_UP_SPRITE_INDEX]],
                      self.tileIdToTile[agentInfo[AGENT_DOWN_SPRITE_INDEX]],
                      self.tileIdToTile[agentInfo[AGENT_LEFT_SPRITE_INDEX]],
                      self.tileIdToTile[agentInfo[AGENT_RIGHT_SPRITE_INDEX]]]


            e = Agent(agentInfo[AGENT_NAME_INDEX], eTiles, eTiles)

            e.setPosition(int(agentInfo[AGENT_X_INDEX]),
                          int(agentInfo[AGENT_Y_INDEX]))

            self.agents.append(e)


        # now read in the action file
        f = open(actionFile)
        lines = f.readlines()

        self.actions = []
        currAction = None
        
        for line in lines:
            l = line.strip()

            # skip empty lines and comments
            if(len(l) == 0 or l[0]=='#'):
                continue

            words = l.split(' ')

            command = words[0]
            arguments = words[1:]

            # set the starting state
            if(command == ACTION_LANG_INITIAL_STATE):
                self.state = arguments[0]
                #print "Interpreted " + str(l) + " as me starting in state '" + str(arguments[0]) + "'"

            elif(command == ACTION_LANG_START_LIGHT_STATE):
                self.lightState = arguments[0]
                
            elif(command == ACTION_LANG_START_LIGHT):
                self.ambientLight = (int(arguments[0]),
                                     int(arguments[1]),
                                     int(arguments[2]))

            elif(command == ACTION_LANG_START_TORCH):
                self.setTorch(True)                                   

            elif(command == ACTION_LANG_START_TORCH_LIGHT):
                self.torchLight = (int(arguments[0]),
                                     int(arguments[1]),
                                     int(arguments[2]))


            # start a new action
            elif(command == ACTION_LANG_BEGIN_ACTION):
                currAction = Action(arguments[0])

            elif(command == ACTION_LANG_INVERT_LIGHTING):
                currAction.setInvertLighting(True)

            elif(command == ACTION_LANG_SET_LIGHT):
                currAction.setLight(int(arguments[0]),
                                    int(arguments[1]),
                                    int(arguments[2]))

            elif(command == ACTION_LANG_CHANGE_LIGHT_STATE):
                currAction.setChangeLightState(arguments[0])
                
            # set the state that we have to be in for the action to trigger
            elif(command == ACTION_LANG_WHEN_IN_STATE):
                currAction.setWhenInState(arguments[0])

            elif(command == ACTION_LANG_EVERY_N_FRAMES):
                currAction.setEveryNFrames(int(arguments[0]))
                
            elif(command == ACTION_LANG_WHEN_IN_LIGHT_STATE):
                currAction.setWhenInLightState(arguments[0])
                
            # set the object we have to interact with for the action to trigger
            elif(command == ACTION_LANG_WHEN_INTERACT_WITH):
                currAction.addWhenInteractWith(arguments[0])

            # set the state we change to when the action happens
            elif(command == ACTION_LANG_CHANGE_STATE_TO):
                currAction.setChangeStateTo(arguments[0])

            # create a message when the action happens
            elif(command == ACTION_LANG_MESSAGE):
                currAction.addMessage(' '.join(arguments))

            # change the tile of an object
            elif(command == ACTION_LANG_CHANGE_OBJECT_TILE):
                currAction.addChangeObjectTile(arguments[0], arguments[1])

            # change the dialogue of an object
            elif(command == ACTION_LANG_CHANGE_OBJECT_DIALOGUE):
                currAction.addChangeObjectDialogue(arguments[0], ' '.join(arguments[1:]))

            # go to another level
            elif(command == ACTION_LANG_CHANGE_LEVEL):
                currAction.setChangeLevel(arguments[0])

            # add an objective
            elif(command == ACTION_LANG_OBJECTIVE):
                if(arguments[0] == "none"):
                    currAction.setObjective("")
                else:
                    currAction.setObjective(' '.join(arguments))

            # get the torch
            elif(command == ACTION_LANG_GET_TORCH):
                currAction.setGetTorch(True)
            
            # complete an action
            elif(command == ACTION_LANG_END_ACTION):
                self.actions.append(currAction)
                currAction = None
                

            else:
                print "ERROR: Unrecognised ACTION_LANG line " + line


    def checkActionTriggers(self, interactedWith, frameCount):
        (s, ls) = (self.state, self.lightState)
        for a in self.actions:
            if(a.triggeredBy(s, ls, interactedWith, frameCount)):
               a.performAction(self)

    def changeObjectTile(self, objectName, newTileName):
        # find the object and reset its tile
        for o in self.objects:
            if(o.name == objectName):
                tile = self.tileIdToTile[newTileName]
                o.tile = tile

    def changeObjectDialogue(self, objectName, newDialogue):
        # find the object and reset its tile
        for o in self.objects:
            if(o.name == objectName):
                o.setDialogue(newDialogue)

    def setObjective(self, objective):
        self.objective = objective
        self.hasObjective = True
        print "set an objective: " + self.objective


    def cancelObjective(self):
        self.hasObjective = False
        self.objective = ""

    def getObjective(self):
        return self.objective

    def changeLevel(self, level):
        # send a message to the overworld handler that we want to end the level
        print "level changed!"
        self.readyForNextLevel = True
        self.nextLevel = level
                
    def addMessage(self, message):
        self.messages.append(message)

    def emptyMessages(self):
        self.messages = []

    def getMessages(self):
        return self.messages

    def setTorch(self, val):
        self.torchOn = True

    def getTorchPercentage(self):
        (r, g, b) = self.torchLight
        return (r/255.0)*100.0

    def needTorchLighting(self):
        (r, g, b) = self.torchLight
        (ar, ag, ab) = self.ambientLight
        return(ar<r or ag<g or ab<b)

    def getTorchLight(self):
        (r, g, b) = self.torchLight
        (ar, ag, ab) = self.ambientLight

        return(max(r, ar), max(g, ag), max(b, ab))
    
    def chargeTorch(self, amount):
        self.torchLight = map(lambda x: x+amount, self.torchLight)
        self.torchLight = map(lambda x: min(255, x), self.torchLight)
        self.torchLight = map(lambda x: max(0, x), self.torchLight)
        
    def changeState(self, state):
        print "Changed state from " + self.state + " to " + state
        self.state = state
            
    def getTile(self, x, y):
        return self.grid[y][x]

    def hasTile(self, x, y):
        return (x >= 0 and x < self.width and y >= 0 and y < self.height)

    def getAgents(self):
        return self.agents

    def getObjects(self):
        return self.objects
    
    # should have been set in readFromFile
    def getPlayer(self):
        return self.player

    
    def canWalk(self, x, y, agent):
        # basic check
        if (not self.hasTile(x, y) or self.getTile(x, y).solid):
            return False

        # check objects
        for o in self.objects:
            if(o.x == x and o.y == y and o.getTile().solid):
                return False

        for a in self.agents:
            if (not (a == agent) and not a in agent.getRecruits() and a.x == x and a.y == y):
                return False

        return True


    def agentAt(self, x, y):
        for a in self.agents:
            if(a.x == x and a.y == y):
                return a

        return None

    def objectAt(self, x, y):
        for o in self.objects:
            if(o.x == x and o.y == y):
                return o

        return None
