import pygame
from constants import *
from overworld import *




pygame.init()

messageFont = pygame.font.Font("data/font/pokgen1.ttf", 16)


screen = pygame.display.set_mode([GAME_WIDTH, GAME_HEIGHT])
pygame.display.set_caption("Gladiator Manager")

clock = pygame.time.Clock()

print "Gladiator Manager Version " + VERSION

playOverworld(screen, clock, messageFont)








