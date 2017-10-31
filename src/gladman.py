import pygame
from constants import *
from overworld import *
from tiles import *
from level import *

def loadTiles():
    tileIdToTile = {}
    tileIdToTile[0] = Tile("data/tiles/grass1.png", False)
    tileIdToTile[1] = Tile("data/tiles/stone1.png", False)
    tileIdToTile[2] = Tile("data/tiles/void1.png", True)
    tileIdToTile["player1up"] = Tile("data/sprites/player1up.png", True)
    tileIdToTile["player1down"] = Tile("data/sprites/player1down.png", True)
    tileIdToTile["player1left"] = Tile("data/sprites/player1left.png", True)
    tileIdToTile["player1right"] = Tile("data/sprites/player1right.png", True)
    tileIdToTile["enemy1"] = Tile("data/sprites/enemy1.png", True)
    return tileIdToTile

pygame.init()

# load fonts
messageFont = pygame.font.Font("data/font/pokgen1.ttf", 16)
nameFont = pygame.font.Font("data/font/pokgen1.ttf", 12)

# load tiles
tileIdToTile = loadTiles()


screen = pygame.display.set_mode([GAME_WIDTH, GAME_HEIGHT])
pygame.display.set_caption("Gladiator Manager")

clock = pygame.time.Clock()

print "Gladiator Manager Version " + VERSION

l1 = Level("", tileIdToTile)
playOverworld(screen, clock, l1, messageFont, nameFont)








