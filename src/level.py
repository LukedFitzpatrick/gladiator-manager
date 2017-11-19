from tiles import *
from agent import *
from loadTiles import *
from random import randint
from converser import *
from tiles import *
from object import *
from action import *
from fighter import *
from random import randint
from random import choice

class Level:
    def __init__(self, name, levelFile, agentFile, objectFile, actionFile, tileIdToTile):
        self.tileIdToTile = tileIdToTile

        self.name = name
        
        self.lightState = ""
        self.state = ""
        self.hasObjective = False
        self.objective = ""

        self.lightingOn = True
        self.ambientLight = (255, 255, 255)

        self.messages = []
        self.readyForNextLevel = False

        self.readFromFile(levelFile, agentFile, objectFile, actionFile)
        #self.procedurallyBuild(32, 32)

    # todo pass in generation parameters here
    def procedurallyBuild(self, width, height):
        self.width = width
        self.height = height

        self.agents = []
        self.objects = []
        
        # grid
        self.grid = []
        for y in range(0, height):
            newline = []
            for x in range(0, width):
                newline.append(self.pcgInitialFillTile())
                #newline.append(self.pcgFloorTile())
                
            self.grid.append(newline)


        # build rooms
        self.pcgBuildSpace()

        
        # put the player on a random non-solid tile
        (playerX, playerY) = (0, 0)
        while(not self.canWalk(playerX, playerY, None)):
            (playerX, playerY) = (randint(0, self.width-1), randint(0, self.height-1))

        self.player = self.createPlayerAgent(playerX,playerY,"down")
        self.agents.append(self.player)

        # actions
        self.actions = []

        # lighting
        self.ambientLight = (110, 100, 100)
        



    def pcgFillRectangle(self, xStart, yStart, width, height):
        for x in range(xStart, xStart+width):
            for y in range(yStart, yStart+height):
                self.grid[y][x] = self.pcgFloorTile()

    
    def pcgBuildSpace(self):
        #numRooms = randint(PCG_ROOMS_MIN, PCG_ROOMS_MAX)
        numRooms = 15
        
        # start with a completely random room
        width = randint(PCG_ROOM_WIDTH_MIN, PCG_ROOM_WIDTH_MAX)
        height = randint(PCG_ROOM_HEIGHT_MIN, PCG_ROOM_HEIGHT_MAX)

        xStart = randint(0, self.width-width)
        yStart = randint(0, self.height-height)

        # build the first room
        self.pcgFillRectangle(xStart, yStart, width, height)

        prevRooms = [pygame.Rect(xStart, yStart, width, height)]
        
        roomsBuilt = 1
        
        # build subsequent rooms
        while(roomsBuilt < numRooms):
            width = randint(PCG_ROOM_WIDTH_MIN, PCG_ROOM_WIDTH_MAX)
            height = randint(PCG_ROOM_HEIGHT_MIN, PCG_ROOM_HEIGHT_MAX)

            xStart = randint(0, self.width-width)
            yStart = randint(0, self.height-height)

            collided = False
            thisRect = pygame.Rect(xStart, yStart, width, height)
            for r in prevRooms:
                if(thisRect.colliderect(r)):
                    collided = True

            if(not collided):
                roomsBuilt += 1
                self.pcgFillRectangle(xStart, yStart, width, height)
                self.pcgJoinRooms(thisRect, prevRooms[-1])
                prevRooms.append(thisRect)

                self.spawnEnemiesInsideRoom(thisRect)

                
    def pcgJoinRooms(self, r1, r2):
        (startX, startY) = (int(r1.centerx), int(r1.centery))
        (finishX, finishY) = (int(r2.centerx), int(r2.centery))
        
        self.pcgBuildCorridor(startX, startY, finishX, finishY)

                
    def pcgBuildCorridor(self, startX, startY, finishX, finishY):
        x = startX
        y = startY

        while(x != finishX or y != finishY):
            self.grid[y][x] = self.pcgCorridorTile()

            yDiff = finishY - y
            xDiff = finishX - x

            if(abs(xDiff) > abs(yDiff)):
                if(x<finishX):
                    x += 1
                elif(x>finishX):
                    x -= 1
            else:
                if(y<finishY):
                    y += 1
                elif(y > finishY):
                    y -= 1
            
    # pass in biome etc.?
    def pcgInitialFillTile(self):
        return self.tileIdToTile["eyewall1"]


    def pcgFloorTile(self):
        return self.tileIdToTile["tiles1"]

    def pcgCorridorTile(self):
        return self.tileIdToTile["tiles1"]


    def spawnEnemiesInsideRoom(self, rect):
        for i in range(0, randint(PCG_ROOM_MIN_ENEMIES, PCG_ROOM_MAX_ENEMIES)):
            (enemyX, enemyY) = (-1, -1)

            while(not self.canWalk(enemyX, enemyY, None)):
                (enemyX, enemyY) = (randint(rect.left, rect.right),
                                    randint(rect.top, rect.bottom))

            self.spawnEnemyAt(enemyX, enemyY)

            
    def spawnEnemyAt(self, x, y):
        sprites = [self.tileIdToTile["goonup"],
                   self.tileIdToTile["goondown"],
                   self.tileIdToTile["goonleft"],
                   self.tileIdToTile["goonright"]]

        knifeSprites = [self.tileIdToTile["goonupknife"],
                        self.tileIdToTile["goondownknife"],
                        self.tileIdToTile["goonleftknife"],
                        self.tileIdToTile["goonrightknife"]]

        f = Fighter("GoonFighter", PLAYER_START_HEALTH, PLAYER_KNIFE_DAMAGE)
        ai = AI(TEAM_EYE_CORPORATION, GOON_AI_PLAN)
        a = Agent("Goon", sprites, knifeSprites, f, ai)
        
        a.facing = choice(["up", "down", "left", "right"])
        a.setPosition(x, y)
        a.hasTorch = True
        a.torchLight = (randint(200, 255),randint(100, 200),randint(100,200))
        a.torchOn = True
        a.hasKnife = True

        self.agents.append(a)
        return a
        


    
    def createPlayerAgent(self, x, y, facing):
        sprites = [self.tileIdToTile["player1up"],
                   self.tileIdToTile["player1down"],
                   self.tileIdToTile["player1left"],
                   self.tileIdToTile["player1right"]]

        knifeSprites = [self.tileIdToTile["player1upknife"],
                        self.tileIdToTile["player1downknife"],
                        self.tileIdToTile["player1leftknife"],
                        self.tileIdToTile["player1rightknife"]]

        f = Fighter("PlayerFighter", PLAYER_START_HEALTH, PLAYER_KNIFE_DAMAGE)
        ai = AI(TEAM_ALLY, NO_AI_PLAN)
        player = Agent("You", sprites, knifeSprites, f, ai)

        player.facing = facing
        player.setPosition(x, y)
        player.hasTorch = True
        player.torchLight = (255,255,255)
        player.hasKnife = True
        
        return player



    
    def readFromFile(self, levelFile, agentFile, objectFile, actionFile):
        # build the basic grid
        f = open(levelFile)
        lines = f.readlines()
        self.grid = []
        for line in lines:
            l = line.split(',')
            newl = []
            for i in l:
                newl.append(self.tileIdToTile[int(i)])
            self.grid.append(newl)
        
        self.width = len(self.grid[0])
        self.height = len(self.grid)


        # read in the objects
        f = open(objectFile)
        lines = f.readlines()
        self.objects = []

        for line in lines:
            objectInfo = line.split(',')
                    
            tile = self.tileIdToTile[objectInfo[OBJECT_SPRITE_INDEX]]

            dialogue = objectInfo[OBJECT_DIALOGUE_INDEX].replace("*comma*", ",")
            o = Object(objectInfo[OBJECT_NAME_INDEX], tile, dialogue)

            o.setPosition(int(objectInfo[OBJECT_X_INDEX]),
                          int(objectInfo[OBJECT_Y_INDEX]))

            self.objects.append(o)
        
        # read in the agents
        f = open(agentFile)
        lines = f.readlines()
        self.agents = []
        
        for line in lines:
            agentInfo = line.split(',')

            name = agentInfo[AGENT_NAME_INDEX]

            health = int(agentInfo[AGENT_HEALTH_INDEX])
            knifeDamage = int(agentInfo[AGENT_KNIFE_DAMAGE_INDEX])

            
            eTiles = [self.tileIdToTile[agentInfo[AGENT_UP_SPRITE_INDEX]],
                      self.tileIdToTile[agentInfo[AGENT_DOWN_SPRITE_INDEX]],
                      self.tileIdToTile[agentInfo[AGENT_LEFT_SPRITE_INDEX]],
                      self.tileIdToTile[agentInfo[AGENT_RIGHT_SPRITE_INDEX]]]


            eKnifeTiles = [self.tileIdToTile[agentInfo[AGENT_UP_KNIFE_SPRITE_INDEX]],
                            self.tileIdToTile[agentInfo[AGENT_DOWN_KNIFE_SPRITE_INDEX]],
                            self.tileIdToTile[agentInfo[AGENT_LEFT_KNIFE_SPRITE_INDEX]],
                            self.tileIdToTile[agentInfo[AGENT_RIGHT_KNIFE_SPRITE_INDEX]]]


            f = Fighter(name + "Fighter", health, knifeDamage)

            if(agentInfo[AGENT_TEAM_INDEX] == "Ally"):
                team = TEAM_ALLY
            elif(agentInfo[AGENT_TEAM_INDEX] == "EyeCorporation"):
                team = TEAM_EYE_CORPORATION

            if(agentInfo[AGENT_AI_INDEX] == "Goon"):
                plan = GOON_AI_PLAN
            else:
                plan = NO_AI_PLAN
                
            ai = AI(team, plan)
            e = Agent(name, eTiles, eKnifeTiles, f, ai)
            ai.setAgent(e)

            e.facing = agentInfo[AGENT_FACING_INDEX]
            
            e.setPosition(int(agentInfo[AGENT_X_INDEX]),
                          int(agentInfo[AGENT_Y_INDEX]))

            self.agents.append(e)

        # everyone has a torch
        for a in self.agents[1:]:
            a.hasTorch = True
            a.torchOn = True
            if(a.ai.team == TEAM_EYE_CORPORATION):
                a.torchLight = (random.randint(200, 255),
                                random.randint(50,150),
                                random.randint(50,150))
            else:
                a.torchLight = (255,255,255)

            
        self.player = self.agents[0]
        self.player.ai.team = TEAM_ALLY

        # now read in the action file
        f = open(actionFile)
        lines = f.readlines()

        self.actions = []
        currAction = None
        
        for line in lines:
            l = line.strip()

            # skip empty lines and comments
            if(len(l) == 0 or l[0]=='#'):
                continue

            words = l.split(' ')

            command = words[0]
            arguments = words[1:]

            # set the starting state
            if(command == ACTION_LANG_INITIAL_STATE):
                self.state = arguments[0]
                #print "Interpreted " + str(l) + " as me starting in state '" + str(arguments[0]) + "'"

            elif(command == ACTION_LANG_START_LIGHT_STATE):
                self.lightState = arguments[0]
                
            elif(command == ACTION_LANG_START_LIGHT):
                self.ambientLight = (int(arguments[0]),
                                     int(arguments[1]),
                                     int(arguments[2]))

            elif(command == ACTION_LANG_START_TORCH):
                self.getPlayer().setHasTorch(True)

            elif(command == ACTION_LANG_START_KNIFE):
                self.getPlayer().setHasKnife(True)
                
            elif(command == ACTION_LANG_START_TORCH_ON):
                self.getPlayer().torchOn = True
                
            elif(command == ACTION_LANG_START_TORCH_LIGHT):
                self.getPlayer().setTorchLight = (int(arguments[0]),
                                     int(arguments[1]),
                                     int(arguments[2]))


            # start a new action
            elif(command == ACTION_LANG_BEGIN_ACTION):
                currAction = Action(arguments[0])

            elif(command == ACTION_LANG_INVERT_LIGHTING):
                currAction.setInvertLighting(True)

            elif(command == ACTION_LANG_SET_LIGHT):
                currAction.setLight(int(arguments[0]),
                                    int(arguments[1]),
                                    int(arguments[2]))

            elif(command == ACTION_LANG_CHANGE_LIGHT_STATE):
                currAction.setChangeLightState(arguments[0])
                
            # set the state that we have to be in for the action to trigger
            elif(command == ACTION_LANG_WHEN_IN_STATE):
                currAction.setWhenInState(arguments[0])

            elif(command == ACTION_LANG_EVERY_N_FRAMES):
                currAction.setEveryNFrames(int(arguments[0]))
                
            elif(command == ACTION_LANG_WHEN_IN_LIGHT_STATE):
                currAction.setWhenInLightState(arguments[0])
                
            # set the object we have to interact with for the action to trigger
            elif(command == ACTION_LANG_WHEN_INTERACT_WITH):
                currAction.addWhenInteractWith(arguments[0])

            elif(command == ACTION_LANG_WHEN_AGENT_DIES):
                currAction.addWhenAgentDies(arguments[0])
                
            # set the state we change to when the action happens
            elif(command == ACTION_LANG_CHANGE_STATE_TO):
                currAction.setChangeStateTo(arguments[0])

            # create a message when the action happens
            elif(command == ACTION_LANG_MESSAGE):
                currAction.addMessage(' '.join(arguments).replace("*comma*", ","))

            # change the tile of an object
            elif(command == ACTION_LANG_CHANGE_OBJECT_TILE):
                currAction.addChangeObjectTile(arguments[0], arguments[1])

            # change the dialogue of an object
            elif(command == ACTION_LANG_CHANGE_OBJECT_DIALOGUE):
                currAction.addChangeObjectDialogue(arguments[0], ' '.join(arguments[1:]))

            # go to another level
            elif(command == ACTION_LANG_CHANGE_LEVEL):
                currAction.setChangeLevel(arguments[0])

            # add an objective
            elif(command == ACTION_LANG_OBJECTIVE):
                if(arguments[0] == "none"):
                    currAction.setObjective("")
                else:
                    currAction.setObjective(' '.join(arguments))

            elif(command == ACTION_LANG_WHEN_ONLY_PLAYER_SURVIVES):
                currAction.setWhenOnlyPlayerSurvives(True)
                
            # get the torch
            elif(command == ACTION_LANG_GET_TORCH):
                currAction.setGetTorch(True)

            elif(command == ACTION_LANG_GET_KNIFE):
                currAction.setGetKnife(True)
                
            # complete an action
            elif(command == ACTION_LANG_END_ACTION):
                self.actions.append(currAction)
                currAction = None
                

            else:
                print "ERROR: Unrecognised ACTION_LANG line " + line


    def checkActionTriggers(self, interactedWith, frameCount, deaths):
        (s, ls) = (self.state, self.lightState)
        for a in self.actions:
            if(a.triggeredBy(self, s, ls, interactedWith, frameCount, deaths, self.agents)):
               a.performAction(self)

    def changeObjectTile(self, objectName, newTileName):
        # find the object and reset its tile
        for o in self.objects:
            if(o.name == objectName):
                tile = self.tileIdToTile[newTileName]
                o.tile = tile

    def changeObjectDialogue(self, objectName, newDialogue):
        # find the object and reset its tile
        for o in self.objects:
            if(o.name == objectName):
                o.setDialogue(newDialogue)

    def setObjective(self, objective):
        self.objective = objective
        self.hasObjective = True
        print "set an objective: " + self.objective


    def cancelObjective(self):
        self.hasObjective = False
        self.objective = ""

    def getObjective(self):
        return self.objective

    def changeLevel(self, level):
        # send a message to the overworld handler that we want to end the level
        print "level changed!"
        self.readyForNextLevel = True
        self.nextLevel = level
                
    def addMessage(self, message):
        self.messages.append(message)

    def emptyMessages(self):
        self.messages = []

    def getMessages(self):
        return self.messages
            
    def changeState(self, state):
        print "Changed state from " + self.state + " to " + state
        self.state = state
            
    def getTile(self, x, y):
        return self.grid[y][x]

    def hasTile(self, x, y):
        return (x >= 0 and x < self.width and y >= 0 and y < self.height)

    def getAgents(self):
        return self.agents

    def getObjects(self):
        return self.objects
    
    # should have been set in readFromFile
    def getPlayer(self):
        return self.player

    
    def canWalk(self, x, y, agent):
        # basic check
        if (not self.hasTile(x, y) or self.getTile(x, y).solid):
            return False

        # check objects
        for o in self.objects:
            if(o.x == x and o.y == y and o.getTile().solid):
                return False

        for a in self.agents:
            if (not (a == agent) and a.x == x and a.y == y):
                return False

        return True


    def agentAt(self, x, y):
        for a in self.agents:
            if(a.x == x and a.y == y):
                return a

        return None

    def objectAt(self, x, y):
        for o in self.objects:
            if(o.x == x and o.y == y):
                return o

        return None


    def updateDeadAgents(self):
        stillAlive = []
        nowDead = []
        # check for deaths
        for a in self.agents:
            if (not a.fighter.alive):
                nowDead.append(a)
            else:
                stillAlive.append(a)

        self.agents = stillAlive
        return nowDead


    def moveAllObjects(self, deltaX, deltaY):
        for o in self.objects:
            o.x += deltaX
            o.y += deltaY

    def moveAllAgents(self, deltaX, deltaY):
        for a in self.agents:
            a.x += deltaX
            a.y += deltaY

    def placeTileInGrid(self, tile, x, y):
        # check if we need to expand the grid size

        (xScrollCount, yScrollCount) = (0, 0)
        
        while(x < 0):
            newGrid = []
            for line in self.grid:
                newGrid.append([self.tileIdToTile[0]] + line)
            x += 1
            
            self.width += 1
            xScrollCount += 1
            self.moveAllObjects(1, 0)
            self.moveAllAgents(1, 0)
            self.grid = newGrid


        while(y < 0):
            newLine = []
            for i in range(0, self.width):
                newLine.append(self.tileIdToTile[0])

            y += 1
                
            self.height += 1
            yScrollCount += 1
            self.moveAllObjects(0, 1)
            self.moveAllAgents(0, 1)
            self.grid = [newLine] + self.grid

            
        if(x >= self.width):
            for i in range(0, (x+1)-self.width):
                for line in self.grid:
                    line.append(self.tileIdToTile[0])
                self.width += 1
            

        if(y >= self.height):
            for i in range(0, (y+1)-self.height):
                newLine = []
                for i in range(0, self.width):
                    newLine.append(self.tileIdToTile[0])

                self.grid.append(newLine)
                self.height += 1

        

        self.grid[y][x] = tile
        return (xScrollCount, yScrollCount)
