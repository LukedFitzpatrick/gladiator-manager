from constants import *
import random

class AI:
    def __init__(self, team, plan):
        self.cooldown = 0
        self.speed = 10
        self.state = AI_STATE_CLOSE_PATROL
        self.team = team
        self.agent = None
        self.plan = plan

    def setAgent(self, agent):
        self.agent = agent
        
    def runAI(self, level):
        self.updateState(level)

        if(self.cooldown == 0):
            self.cooldown = self.speed

            # make a move
            if(self.state == AI_STATE_STAND_STILL):
                return(AI_NOTHING)
            
            elif(self.state == AI_STATE_CLOSE_PATROL):
                return self.randChoiceWithDistribution(
                    [(AI_NOTHING,10), (AI_MOVE_DOWN,1), (AI_MOVE_UP,1),
                     (AI_MOVE_LEFT,1), (AI_MOVE_RIGHT,1)])

            elif(self.state == AI_STATE_KNIFE):
                return AI_KNIFE
            
        else:
            self.cooldown -= 1
                
    def updateState(self, level):
        # the goons: just stab when you can, wander around otherwise
        if(self.plan == GOON_AI_PLAN):
            if(self.facingEnemyDirectly(level)):
                self.state = AI_STATE_KNIFE
                self.cooldown = 0
            else:
                self.state = AI_STATE_CLOSE_PATROL


    def facingEnemyDirectly(self, level):
        # if an enemy is standing right in front of us...
        (faceX, faceY) = self.agent.faceTile()

        a = level.agentAt(faceX, faceY)
        if(a != None and a.ai.team != self.team):
            return True

        return False


    
    def randChoiceWithDistribution(self, choices):
        pos = []
        for c in choices:
            (choice, numChances) = c
            for i in range(0, numChances):
                pos.append(choice)

        return random.choice(pos)
