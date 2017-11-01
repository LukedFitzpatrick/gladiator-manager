import pygame

class Tile:
    def __init__(self, imgPaths, solid):
        self.imgs = []
        for p in imgPaths:
            self.imgs.append(pygame.image.load(p))

        self.currFrame = 0
        self.maxFrame = len(self.imgs) 
            
        self.solid = solid

    def getImage(self):
        # todo animations go here
        self.currFrame = (self.currFrame + 1) % self.maxFrame
        return self.imgs[self.currFrame]
    
    
    

