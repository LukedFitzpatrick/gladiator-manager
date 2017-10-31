import pygame
from constants import *
from overworld import *
from tiles import *
from level import *



pygame.init()

# load fonts
messageFont = pygame.font.Font("data/font/pokgen1.ttf", 16)

# load tiles
loadTiles()

screen = pygame.display.set_mode([GAME_WIDTH, GAME_HEIGHT])
pygame.display.set_caption("Gladiator Manager")

clock = pygame.time.Clock()

print "Gladiator Manager Version " + VERSION

l1 = Level("")
playOverworld(screen, clock, l1, messageFont)








