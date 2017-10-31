import pygame

class Tile:
    def __init__(self, imgPath, solid):
        self.img = pygame.image.load(imgPath)
        self.solid = solid


tileIdToTile = {}

def loadTiles():
    tileIdToTile[0] = Tile("data/tiles/grass1.png", False)
    tileIdToTile[1] = Tile("data/tiles/stone1.png", False)
    tileIdToTile[2] = Tile("data/tiles/void1.png", True)
    
    
def getTile(tileId):
    return tileIdToTile[tileId]
