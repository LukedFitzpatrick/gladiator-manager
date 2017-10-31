from tiles import *
from random import randint

class Level:
    def __init__(self, levelFile):
        self.readFromFile(levelFile)

    def readFromFile(self, levelFile):
        # todo make this actually read from a level file
        self.grid = []
        
        for row in range(0, 20):
            row = []
            for column in range(0, 20):
                row.append(getTile(randint(0, 2)))

            self.grid.append(row)

        self.width = len(self.grid[0])
        self.height = len(self.grid)
            
    def getTile(self, x, y):
        return self.grid[y][x]

    def hasTile(self, x, y):
        return (x >= 0 and x < self.width and y >= 0 and y < self.height)
        
