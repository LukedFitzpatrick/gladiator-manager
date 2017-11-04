import pygame
from constants import *
from overworld import *
from tiles import *
from level import *

def loadTiles(tileFile):
    f = open(tileFile)
    lines = f.readlines()

    tileIdToTile = {}

    
    for l in lines:
        tileData = l.split(',')
        if(tileData[TILE_ID_INDEX].isdigit()):
            key = int(tileData[TILE_ID_INDEX])
        else:
            key = tileData[TILE_ID_INDEX]

        if(tileData[TILE_SOLID_INDEX] == "True"):
            solid = True
        else:
            solid = False

        d = tileData[TILE_IMAGE_PATH_INDEX]
        if(d[0] == '[' and d[-1] == ']'):
            print "Found an animated sprite"
            frames = d[1:-1].split(' ')
            tileIdToTile[key] = Tile(frames, solid)
        else:
            tileIdToTile[key] = Tile([d], solid)

    return tileIdToTile

pygame.init()

# load fonts
messageFont = pygame.font.Font("data/font/pokgen1.ttf", 16)
nameFont = pygame.font.Font("data/font/pokgen1.ttf", 12)
damageFont = pygame.font.Font("data/font/pokgen1.ttf", 8)

# load tiles
tileIdToTile = loadTiles("data/tilelist.txt")


screen = pygame.display.set_mode([GAME_WIDTH, GAME_HEIGHT])
pygame.display.set_caption(VERSION)

clock = pygame.time.Clock()

print "Version " + VERSION


nextLevel = "room1"
#nextLevel = "combatTestZone"
while True:
    l = Level("data/levels/"+ nextLevel + "/" + nextLevel + ".lvl",
              "data/levels/"+ nextLevel + "/" + nextLevel + ".age",
              "data/levels/"+ nextLevel + "/" + nextLevel + ".obj",
              "data/levels/"+ nextLevel + "/" + nextLevel + ".act",
              tileIdToTile)

    o = Overworld()
    nextLevel = o.playOverworld(screen, clock, l, messageFont, nameFont, damageFont)








