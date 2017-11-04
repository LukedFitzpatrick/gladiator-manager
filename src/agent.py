from constants import *
from ai import *
import random

class Agent:
    def __init__(self, name, tiles, attackTiles, fighter, ai, facing="down"):
        self.tiles = tiles
        self.fighter = fighter
        self.facing = facing

        self.hasKnife = False
        self.currentlyKnifing = False
        
        self.recruits = []
        
        self.following = None
        self.follower = None
        
        self.attackTiles = attackTiles

        self.currTiles = self.tiles

        self.ai = ai
        
        self.facingToTileMap = {}
        self.facingToTileMap["up"] = 0
        self.facingToTileMap["down"] = 1
        self.facingToTileMap["left"] = 2
        self.facingToTileMap["right"] = 3
        
        self.name = name

        self.width = 32
        self.height = 32


        self.torchOn = False
        self.hasTorch = False
        self.torchLight = (255, 255, 255)
        
        # etc.

        self.knifeFrames = 0


    def setHasKnife(self, value):
        self.hasKnife = value

    def setHasTorch(self, value):
        self.hasTorch = value

    def setTorchOn(self, value):
        self.torchOn = value

    def setTorchLight(self, value):
        self.torchLight = value

    def flipTorch(self):
        self.torchOn = not self.torchOn

        
    def runAI(self, level):
        return self.ai.runAI(level)
    
    def updateFrames(self):
        if(self.knifeFrames > 0):
            self.knifeFrames -= 1

            if(self.knifeFrames == 0):
                self.endAttack()

    def startAttack(self):
        if(self.knifeFrames == 0):
            self.knifeFrames = KNIFE_FRAMES
            self.currTiles = self.attackTiles
            self.currentlyKnifing = True

    def endAttack(self):
        self.currTiles = self.tiles
        self.currentlyKnifing = False

    def dealDamage(self, damage, fromX, fromY):
        self.fighter.dealDamage(damage)
        self.ai.gettingAttackedFrom(fromX, fromY)
        
    def getName(self):
        return self.name
    
    def getImage(self):
        # todo animations go here
        return self.currTiles[self.facingToTileMap[self.facing]].getImage()

    
    def setPosition(self, x, y):
        self.x = x
        self.y = y


    def addRecruit(self, a):
        if(len(self.recruits) == 0):
            a.setMaster(self)
            self.follower = a
        else:
            nextUp = self.recruits[len(self.recruits)-1]
            a.setMaster(nextUp)
            nextUp.follower = a
            

        self.recruits.append(a)


    def getRecruits(self):
        return self.recruits
        
    def setMaster(self, a):
        self.following = a

    def getMaster(self):
        return self.following

        
    def faceTile(self):
        if(self.facing == "right"):
            return (self.x+1, self.y)
        elif(self.facing == "left"):
            return (self.x-1, self.y)
        elif(self.facing == "up"):
            return (self.x, self.y-1)
        elif(self.facing == "down"):
            return (self.x, self.y+1)
        else:
            print "Agent.py, faceTile(): Something terrible has happened"
        
            
    
        
    def translate(self, deltaX, deltaY, level):
        projectedX = self.x + deltaX
        projectedY = self.y + deltaY

        oldX = self.x
        oldY = self.y

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

            # move recruits
            #for a in self.recruits:
            if(self.follower):
                a = self.follower
                a.translate(oldX - a.x, oldY - a.y, level)

            
    def getDialogue(self, conversationState):
        return self.converser.getDialogue(conversationState)
