from constants import *

class Object:
    def __init__(self, name, tile, dialogue):
        self.name = name
        self.tile = tile
        self.dialogue = dialogue

        self.width = TILE_WIDTH
        self.height = TILE_HEIGHT

    def getImage(self):
        return self.tile.getImage()

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def getName(self):
        return self.name

    def getTile(self):
        return self.tile

    def getDialogue(self):
        return self.dialogue
