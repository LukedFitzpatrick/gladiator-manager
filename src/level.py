from tiles import *
from agent import *
from loadTiles import *
from random import randint




class Level:
    def __init__(self, levelFile, tileIdToTile):
        self.tileIdToTile = tileIdToTile
        self.readFromFile(levelFile)
        
    def readFromFile(self, levelFile):
        # todo make this actually read from a level file
        self.grid = []
        
        for row in range(0, 20):
            row = []
            agentRow = []
            
            for column in range(0, 20):
                row.append(self.tileIdToTile[randint(0, 2)])
                agentRow.append(None)

            self.grid.append(row)

            
        self.width = len(self.grid[0])
        self.height = len(self.grid)

        # now make the agent list
        self.agents = []
        self.player = self.tileIdToTile["player"]
        self.player.setPosition(0, 0)
        
        self.agents.append(self.player)
            
    def getTile(self, x, y):
        return self.grid[y][x]

    def hasTile(self, x, y):
        return (x >= 0 and x < self.width and y >= 0 and y < self.height)

    def getAgents(self):
        return self.agents

    # should have been set in readFromFile
    def getPlayer(self):
        return self.player
