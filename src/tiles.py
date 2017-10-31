import pygame

class Tile:
    def __init__(self, imgPath, solid):
        self.img = pygame.image.load(imgPath)
        self.solid = solid

    def getImage(self):
        # todo animations go here
        return self.img

