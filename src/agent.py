from constants import *

class Agent:
    def __init__(self, name, tiles, facing="down"):
        self.tiles = tiles

        self.facing = facing
        
        self.facingToTileMap = {}
        self.facingToTileMap["up"] = tiles[0]
        self.facingToTileMap["down"] = tiles[1]
        self.facingToTileMap["left"] = tiles[2]
        self.facingToTileMap["right"] = tiles[3]
        
        self.name = name

        self.width = 32
        self.height = 32

        # etc.


    def getName(self):
        return self.name
    
    def getImage(self):
        # todo animations go here
        return self.facingToTileMap[self.facing].getImage()

    
    def setPosition(self, x, y):
        self.x = x
        self.y = y


    def translate(self, deltaX, deltaY, level):
        projectedX = self.x + deltaX
        projectedY = self.y + deltaY



        if(projectedX > self.x):
            if(CAN_TURN_ON_THE_SPOT and self.facing != "right"):
                projectedX = self.x
            self.facing = "right"

        elif(projectedX < self.x):
            if(CAN_TURN_ON_THE_SPOT and self.facing != "left"):
                projectedX = self.x
            self.facing = "left"

        if(projectedY > self.y):
            if(CAN_TURN_ON_THE_SPOT and self.facing != "down"):
                projectedY = self.y

            self.facing = "down"

        elif(projectedY < self.y):
            if(CAN_TURN_ON_THE_SPOT and self.facing != "up"):
                projectedY = self.y

            self.facing = "up"

        if(level.canWalk(projectedX, projectedY, self)):
            self.x = projectedX
            self.y = projectedY


        
    def setDialogue(self, dialogue):
        self.dialogue = dialogue
    



