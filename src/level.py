from tiles import *
from agent import *
from loadTiles import *
from random import randint
from converser import *
from tiles import *
from object import *

class Level:
    def __init__(self, levelFile, agentFile, objectFile, tileIdToTile):
        self.tileIdToTile = tileIdToTile
        self.readFromFile(levelFile, agentFile, objectFile)
        
    def readFromFile(self, levelFile, agentFile, objectFile):

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
            
            o = Object(objectInfo[OBJECT_NAME_INDEX], tile, objectInfo[OBJECT_DIALOGUE_INDEX])

            o.setPosition(int(objectInfo[OBJECT_X_INDEX]),
                          int(objectInfo[OBJECT_Y_INDEX]))

            self.objects.append(o)
        
        # read in the agents
        f = open(agentFile)
        print agentFile
        lines = f.readlines()
        self.agents = []
        
        # lines[0] should contain the player
        print lines[0]
        playerInfo = lines[0].split(',')
        playerTiles = [self.tileIdToTile[playerInfo[AGENT_UP_SPRITE_INDEX]],
                       self.tileIdToTile[playerInfo[AGENT_DOWN_SPRITE_INDEX]],
                       self.tileIdToTile[playerInfo[AGENT_LEFT_SPRITE_INDEX]],
                       self.tileIdToTile[playerInfo[AGENT_RIGHT_SPRITE_INDEX]]]

        self.player = Agent(playerInfo[AGENT_NAME_INDEX], playerTiles, None)
        print playerInfo
        
        self.player.setPosition(int(playerInfo[AGENT_X_INDEX]),
                                int(playerInfo[AGENT_Y_INDEX]))
        self.agents.append(self.player)

        for line in lines[1:]:
            agentInfo = line.split(',')
            
            eTiles = [self.tileIdToTile[agentInfo[AGENT_UP_SPRITE_INDEX]],
                      self.tileIdToTile[agentInfo[AGENT_DOWN_SPRITE_INDEX]],
                      self.tileIdToTile[agentInfo[AGENT_LEFT_SPRITE_INDEX]],
                      self.tileIdToTile[agentInfo[AGENT_RIGHT_SPRITE_INDEX]]]

            c = Converser(agentInfo[AGENT_CONVERSER_INDEX])
            e = Agent(agentInfo[AGENT_NAME_INDEX], eTiles, c)

            e.setPosition(int(agentInfo[AGENT_X_INDEX]),
                          int(agentInfo[AGENT_Y_INDEX]))

            self.agents.append(e)

                    
            
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
