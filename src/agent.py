from level import *

class Agent:
    def __init__(self, imgPath, name):
        self.img = pygame.image.load(imgPath)
        self.solid = True
        self.name = name

        self.width = 32
        self.height = 32

        # etc.

    def getImage(self):
        # todo animations go here
        return self.img

    
    def setPosition(self, x, y):
        self.x = x
        self.y = y


    def translate(self, deltaX, deltaY, level):
        projectedX = self.x + deltaX
        projectedY = self.y + deltaY

        if(level.hasTile(projectedX, projectedY) and
           not level.getTile(projectedX, projectedY).solid):
            self.x = projectedX
            self.y = projectedY
        
