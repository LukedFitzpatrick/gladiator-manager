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
                row.append(self.tileIdToTile[randint(0, 1)])
                agentRow.append(None)

            self.grid.append(row)

            
        self.width = len(self.grid[0])
        self.height = len(self.grid)

        # now make the agents list
        self.agents = []

        # the player
        playerTiles = [self.tileIdToTile["player1up"],
                       self.tileIdToTile["player1down"],
                       self.tileIdToTile["player1left"],
                       self.tileIdToTile["player1right"]]

        self.player = Agent("You", playerTiles)
        self.player.setPosition(0, 0)
        self.agents.append(self.player)

        # some enemies
        for i in range(0, 5):
            eTiles = [self.tileIdToTile["enemy1"],
                           self.tileIdToTile["enemy1"],
                           self.tileIdToTile["enemy1"],
                           self.tileIdToTile["enemy1"]]

            
            e = Agent("Enemy" + str(i), eTiles)
            e.setPosition((2*i)+2, (2*i)+2)
            e.setDialogue("Hello, I'm enemy " + str(i))
            self.agents.append(e)
            
            
    def getTile(self, x, y):
        return self.grid[y][x]

    def hasTile(self, x, y):
        return (x >= 0 and x < self.width and y >= 0 and y < self.height)

    def getAgents(self):
        return self.agents

    # should have been set in readFromFile
    def getPlayer(self):
        return self.player


    def canWalk(self, x, y):
        return hasTile(projectedX, projectedY) and
               not level.getTile(projectedX, projectedY).solid):