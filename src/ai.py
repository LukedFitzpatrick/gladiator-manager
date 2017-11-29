from constants import *
import random

class AI:
    def __init__(self, team, plan):
        self.cooldown = 0
        self.speed = 5
        self.state = AI_STATE_CLOSE_PATROL
        self.team = team
        self.agent = None
        self.plan = plan
        self.knifeCooldown = 0

        self.incomingAttack = False
        self.incomingAttackLocation = (-1, -1)

        self.alerts = []

        self.hasATargetSquare = False
        
        self.statusMark = ""

    def setAgent(self, agent):
        self.agent = agent


    # carries out the actions for each state
    def runAI(self, level):
        self.updateState(level)

        if(self.cooldown == 0):
            self.cooldown = self.speed

            if(self.state == AI_STATE_STAND_STILL):
                return(AI_NOTHING)
            
            elif(self.state == AI_STATE_CLOSE_PATROL):
                return self.randChoiceWithDistribution(
                    [(AI_NOTHING,10), (AI_MOVE_DOWN,1), (AI_MOVE_UP,1),
                     (AI_MOVE_LEFT,1), (AI_MOVE_RIGHT,1)])

            elif(self.state == AI_STATE_KNIFE):
                self.knifeCooldown -= 1
                if(self.knifeCooldown == 0):
                    return AI_KNIFE
                else:
                    return AI_NOTHING

            elif(self.state == AI_STATE_MOVE_TOWARD):
                self.incomingAttack = False
                return self.moveToward(self.moveTowardX, self.moveTowardY, level)
            
            elif(self.state == AI_STATE_WALK_FORWARD):
                return self.directionToMove(self.agent.facing)
        else:
            self.cooldown -= 1


    # choose what state we're in
    def updateState(self, level):
        # basic goon AI: stand still, investigate, attack
        if(self.plan == GOON_AI_PLAN):
            # check if we can see the enemy
            if(self.enemyInDirectLineOfSight(level)):
                self.alert(level.getPlayer().x, level.getPlayer().y)
                self.state = AI_STATE_WALK_FORWARD
                self.statusMark = "!"
                
            elif(self.incomingAttack):
                self.statusMark = "!"
                if(self.agent.faceTile != self.incomingAttackLocation):
                    self.state = AI_STATE_MOVE_TOWARD
                    (self.moveTowardX, self.moveTowardY) = self.incomingAttackLocation
                else:
                    self.enterKnifeState()

            elif(self.facingEnemyDirectly(level)):
                self.statusMark = "!"
                self.enterKnifeState()

            elif(self.hasATargetSquare):
                self.state = AI_STATE_MOVE_TOWARD
                if(self.atDestinationSquare()):
                    self.hasATargetSquare = False
            
            elif(len(self.alerts) > 0):
                alertX, alertY = self.alerts.pop(0)
                self.state = AI_STATE_MOVE_TOWARD
                self.moveTowardX = alertX
                self.moveTowardY = alertY
                self.statusMark = "?"
                self.hasATargetSquare = True
                
            else:
                self.state = AI_STATE_CLOSE_PATROL
                self.statusMark = ""
                #self.state = AI_STATE_STAND_STILL

        # agents with no AI
        elif(self.plan == NO_AI_PLAN):
            self.state = AI_STATE_STAND_STILL


    def atDestinationSquare(self):
        return (self.agent.x == self.moveTowardX and
                self.agent.y == self.moveTowardY)

    
    def moveToward(self, x, y, level):
        if(self.agent.x < x):
            return AI_MOVE_RIGHT

        if(self.agent.x > x):
            return AI_MOVE_LEFT

        if(self.agent.y < y):
            return AI_MOVE_DOWN

        if(self.agent.y > y):
            return AI_MOVE_UP

            # return random.choice([AI_MOVE_RIGHT, AI_MOVE_LEFT,
            #                       AI_MOVE_UP, AI_MOVE_DOWN])

        return AI_NOTHING
            
    # our agent telling us we're getting attacked from a certain spot
    def gettingAttackedFrom(self, x, y):
        self.incomingAttack = True
        self.incomingAttackLocation = (x, y)
    
    def enterKnifeState(self):
        self.state = AI_STATE_KNIFE
        if(self.knifeCooldown == 0):
            self.knifeCooldown = BUTTON_PRESS_SIMULATION_COOLDOWN
        
    def directionToMove(self, direction):
        if(direction == "left"):
            return AI_MOVE_LEFT
        elif(direction == "right"):
            return AI_MOVE_RIGHT
        elif(direction == "up"):
            return AI_MOVE_UP
        elif(direction == "down"):
            return AI_MOVE_DOWN

    def enemyInDirectLineOfSight(self, level):
        (faceX, faceY) = self.agent.faceTile()
        (selfX, selfY) = (self.agent.x, self.agent.y)
                                
        deltaX = faceX - selfX
        deltaY = faceY - selfY

        searchX = selfX
        searchY = selfY
        searchDone = False

        while not searchDone:
            if(not level.canWalk(searchX, searchY, self.agent)):
                searchDone = True
            if(self.isEnemyAt(level, searchX, searchY)):
                return True
            searchX += deltaX
            searchY += deltaY

        return False
        
    def facingEnemyDirectly(self, level):
        # if an enemy is standing right in front of us...
        (faceX, faceY) = self.agent.faceTile()
        a = level.agentAt(faceX, faceY)
        return self.isEnemyAt(level, faceX, faceY)


    def canSee(self, level, x, y):
        (faceX, faceY) = self.agent.faceTile()
        (selfX, selfY) = (self.agent.x, self.agent.y)
        
        deltaX = faceX - selfX
        deltaY = faceY - selfY

        searchX = selfX
        searchY = selfY
        searchDone = False

        while not searchDone:
            if(not level.canWalk(searchX, searchY, self.agent)):
                searchDone = True
            if(searchX == x and searchY == y):
                return True
            searchX += deltaX
            searchY += deltaY

        return False

    
    def isEnemyAt(self, level, x, y):
        a = level.agentAt(x, y)
        if(a != None and a.ai.team != self.team):
            return True
        else:
            return False



    def alert(self, x, y):
        # we get an alert at x y
        self.alerts.append((x,y))
        
    def randChoiceWithDistribution(self, choices):
        pos = []
        for c in choices:
            (choice, numChances) = c
            for i in range(0, numChances):
                pos.append(choice)

        return random.choice(pos)
