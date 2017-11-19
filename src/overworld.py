import pygame
from textrect import *
from constants import *
from agent import *
from random import randint

class Message:
    def __init__(self, text, colour, backgroundColour, font):
        self.text = text
        self.colour = colour
        self.backgroundColour = backgroundColour
        self.font = font  

class Overworld:

    def __init__(self):
        # initialise things
        self.keysdown = []
        self.totalFrameCounter = 0
        self.playerMoveLock = 0
        (self.cameraSlideXPixels, self.cameraSlideYPixels) = (0, 0)
        (self.screenShakeX, self.screenShakeY) = (0, 0)
        (self.screenShakeAmount, self.screenShakeTimer) = (0, 0)
        (self.hazeColour, self.hazeTimer) = ((0, 0, 0), 0)
        self.damageMessages = []
        self.levelEditMode = False
        self.currentTileToPlace = None

    # pops up a message and waits for key press        
    def displayMessage(self, message, options, smallFont):
        currentOptionIndex = 0

        # wait for user to accept the message
        done = False
        while not done:
            self.clock.tick(FRAME_RATE)

            # display the message box
            pygame.draw.rect(self.screen,
                             (255,255,255),
                             (0,GAME_HEIGHT-MESSAGE_HEIGHT,
                              MESSAGE_WIDTH,MESSAGE_HEIGHT), 0)

            pygame.draw.rect(self.screen,
                             (100,100,100),
                             (0,GAME_HEIGHT-MESSAGE_HEIGHT,
                              MESSAGE_WIDTH,MESSAGE_HEIGHT), 10)

            pygame.draw.rect(self.screen,
                             (0,0,0),
                             (0,GAME_HEIGHT-MESSAGE_HEIGHT,
                              MESSAGE_WIDTH,MESSAGE_HEIGHT), 5)

            # word wrap the message into a label
            messageRect = pygame.Rect(TEXT_PADDING_X,
                                      OVERWORLD_HEIGHT+TEXT_PADDING_Y,
                                      MESSAGE_WIDTH-(TEXT_PADDING_X*2),
                                      MESSAGE_HEIGHT-(TEXT_PADDING_Y*2))

            label = render_textrect(message.text,
                                    message.font,
                                    messageRect,
                                    message.colour,
                                    message.backgroundColour,
                                    0)

            self.screen.blit(label,
                             (TEXT_PADDING_X,
                              (OVERWORLD_HEIGHT-MESSAGE_HEIGHT)+TEXT_PADDING_Y))

            pygame.display.flip()


            optionsMessage = options[currentOptionIndex]


            optionText = options[currentOptionIndex]
            if(currentOptionIndex > 0):
                optionText = "<- " + optionText
            if(currentOptionIndex < len(options)-1):
                optionText += " ->"

            label = smallFont.render(optionText, 1, PRESS_ANY_KEY_COLOUR)

            self.screen.blit(label, (PRESS_ANY_KEY_X+TEXT_PADDING_X,
                            GAME_HEIGHT-PRESS_ANY_KEY_HEIGHT-TEXT_PADDING_Y))

            pygame.display.flip()


            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:                   
                    pygame.quit()

                elif event.type == pygame.KEYDOWN:
                    if(event.key == ACCEPT_BUTTON):
                        return options[currentOptionIndex]

                    elif(event.key == RIGHT_BUTTON):
                        currentOptionIndex = (currentOptionIndex+1) % len(options)

                    elif(event.key == LEFT_BUTTON):
                        currentOptionIndex = (currentOptionIndex-1) % len(options)



    def isOnScreen(self, x, y):
        return (x >= 0 and x <= NUM_TILES_X and y >= 0 and y <= NUM_TILES_Y)



    def displayPressEnterMessage(self, screen, font, o):
        label = font.render("<press enter>", 1, (255, 255, 255))
        self.screen.blit(label, (0, 0))


    def screenCoordsToTileCoords(self, (screenX, screenY)):
        tileX = (screenX / TILE_WIDTH) + self.cameraX
        tileY = (screenY / TILE_HEIGHT) + self.cameraY
        return (tileX, tileY)

        
    def runLevelEditor(self):
        label = self.smallFont.render("<editing level>", 1, (255, 255, 255))
        self.screen.blit(label, (0, 0))


        # outline around where we're placing
        (tileX, tileY) = self.screenCoordsToTileCoords(pygame.mouse.get_pos())

        (screenX, screenY) = self.tileCoordsToScreenCoords(tileX, tileY)
        
        pygame.draw.rect(self.screen,(255,0,0),
                         (screenX,screenY,TILE_WIDTH,TILE_HEIGHT), 1)

        
        
        for p in self.clickPos:
            (tileX, tileY) = self.screenCoordsToTileCoords(p)
            self.level.placeTileInGrid(self.currentTileToPlace, tileX, tileY)




        for s in self.scrollDowns:
            self.currentTileIndex += 1

        for s in self.scrollUps:
            self.currentTileIndex -= 1
        
        self.currentTileIndex = self.currentTileIndex % len(self.allTilesList)
        self.currentTileToPlace = self.allTilesList[self.currentTileIndex]
            
        self.scrollDowns = []
        self.scrollUps = []
        self.clickPos = []
            
        if(LEVEL_EDIT_PROMPT_BUTTON in self.keysdown):
            choice = raw_input("(t: place tile) :")
            if(choice == "t"):
                print "Place tile"
                tileChoice = raw_input("Which tile? ")

                if(tileChoice.isdigit()):
                    key = int(tileChoice)
                else:
                    key = tileChoice

                if(tileChoice in self.level.tileIdToTile.keys()):
                    print "Found that!"
                    self.currentTileToPlace = self.level.tileIdToTile[key]
                else:
                    print "Couldn't find that tile."

            else:
                print "Huh?"


        (px, py) = pygame.mouse.get_pos()
        if(self.currentTileToPlace != None):
            self.screen.blit(self.currentTileToPlace.getImage(), (px,py,TILE_WIDTH,TILE_HEIGHT))



        


    def drawDamageMessages(self):
        remainingMessages = []
        for d in self.damageMessages:
            (screenX, screenY, damage, framesLeft, wiggle) = d
            label = self.damageMessageFont.render(str(damage), 1, DAMAGE_MESSAGE_COLOUR)
            self.screen.blit(label, (screenX, screenY))

            if framesLeft > 1:
                remainingMessages.append(
                    (screenX+randint(-wiggle,wiggle),
                     screenY-1,
                     damage,
                     framesLeft-1,
                     wiggle))

        self.damageMessages = remainingMessages




    def tileCoordsToScreenCoords(self, x, y):
        screenX = (x-self.cameraX)*TILE_WIDTH + self.cameraSlideXPixels + self.screenShakeX
        screenY = (y-self.cameraY)*TILE_HEIGHT + self.cameraSlideYPixels + self.screenShakeY    
        return (screenX, screenY)


    def shakeScreen(self, amount, duration):
        self.screenShakeAmount = max(amount, self.screenShakeAmount)
        self.screenShakeTimer = max(duration, self.screenShakeTimer)


    def hazeScreen(self, colour, duration):
        self.hazeColour = colour
        self.hazeTimer = duration


    def updateScreenShake(self):
        if(self.screenShakeTimer > 0):
            self.screenShakeTimer -= 1
            self.screenShakeX = random.choice(range(-self.screenShakeAmount, self.screenShakeAmount))
            self.screenShakeY = random.choice(range(-self.screenShakeAmount, self.screenShakeAmount))
        else:
            (self.screenShakeX, self.screenShakeY) = (0, 0)
                

    def handleTorch(self):
        if(self.level.getPlayer().hasTorch and TORCH_BUTTON in self.keysdown):
            self.keysdown.remove(TORCH_BUTTON)
            self.level.getPlayer().flipTorch()


    def handlePlayerMovement(self):
        # handle key presses
        if (self.playerMoveLock == 0):
            if(LEFT_BUTTON in self.keysdown):
                self.level.getPlayer().translate(-1, 0, self.level)
                self.playerMoveLock = MOVE_LOCK_FRAMES

            elif(RIGHT_BUTTON in self.keysdown):
                self.level.getPlayer().translate(1, 0, self.level)
                self.playerMoveLock = MOVE_LOCK_FRAMES

            elif(UP_BUTTON in self.keysdown):
                self.level.getPlayer().translate(0, -1, self.level)
                self.playerMoveLock = MOVE_LOCK_FRAMES

            elif(DOWN_BUTTON in self.keysdown):
                self.level.getPlayer().translate(0, 1, self.level)
                self.playerMoveLock = MOVE_LOCK_FRAMES
        else:
            self.playerMoveLock = max(self.playerMoveLock-1, 0)



    def runAI(self):
        for a in self.level.agents:
            a.updateFrames()
            if(a != self.level.getPlayer()):
                move = a.runAI(self.level)
                if(move == AI_MOVE_DOWN):
                    a.translate(0, 1, self.level)
                elif(move == AI_MOVE_UP):
                    a.translate(0, -1, self.level)
                elif(move == AI_MOVE_LEFT):
                    a.translate(-1, 0, self.level)
                elif(move == AI_MOVE_RIGHT):
                    a.translate(1, 0, self.level)
                elif(move == AI_KNIFE):
                    a.startAttack()
        
            

    def updateCamera(self):
        (oldCameraX, oldCameraY) = (self.cameraX, self.cameraY)
        self.cameraX = max(0, self.level.getPlayer().x - NUM_TILES_X/2)
        self.cameraY = max(0, self.level.getPlayer().y - NUM_TILES_Y/2)


        self.cameraX = min(self.cameraX, self.level.width-NUM_TILES_X)
        self.cameraY = min(self.cameraY, self.level.height-NUM_TILES_Y)
        
        if(CAMERA_SLIDE_ON):
            if(self.cameraX > oldCameraX):
                self.cameraSlideXPixels += CAMERA_SLIDE_AMOUNT
            elif(self.cameraX < oldCameraX):
                self.cameraSlideXPixels -= CAMERA_SLIDE_AMOUNT
            if(self.cameraY > oldCameraY):
                self.cameraSlideYPixels += CAMERA_SLIDE_AMOUNT
            elif(self.cameraY < oldCameraY):
                self.cameraSlideYPixels -= CAMERA_SLIDE_AMOUNT

            if(self.cameraSlideXPixels < -CAMERA_SLIDE_SPEED):
                self.cameraSlideXPixels += CAMERA_SLIDE_SPEED
            elif(self.cameraSlideXPixels > CAMERA_SLIDE_SPEED):
                self.cameraSlideXPixels -= CAMERA_SLIDE_SPEED
            if(self.cameraSlideYPixels < -CAMERA_SLIDE_SPEED):
                self.cameraSlideYPixels += CAMERA_SLIDE_SPEED
            elif(self.cameraSlideYPixels > CAMERA_SLIDE_SPEED):
                self.cameraSlideYPixels -= CAMERA_SLIDE_SPEED
        


    def renderLevelGrid(self):
        for x in range(self.cameraX-1, self.cameraX+NUM_TILES_X+1):
            for y in range(self.cameraY-1, self.cameraY+NUM_TILES_Y+1):
                (screenX, screenY) = self.tileCoordsToScreenCoords(x, y)

                # draw tiles
                if(self.level.hasTile(x, y)):
                    t = self.level.getTile(x, y)
                    self.screen.blit(t.getImage(), (screenX,screenY,TILE_WIDTH,TILE_HEIGHT))

                    # display hitboxes
                    if(HITBOXES and t.solid):
                        pygame.draw.rect(self.screen,(255,0,0),
                                         (screenX,screenY,TILE_WIDTH,TILE_HEIGHT), 1)

                # out of self.level hitboxes
                else:
                    if(HITBOXES):
                        pygame.draw.rect(self.screen,(0,0,255),
                                         (screenX,screenY,TILE_WIDTH,TILE_HEIGHT), 1)
        

    def drawObjects(self):
        for a in self.level.getObjects():
            projectedX = a.x-self.cameraX
            projectedY = a.y-self.cameraY

            if(self.isOnScreen(projectedX, projectedY)):
                (screenX, screenY) = self.tileCoordsToScreenCoords(a.x, a.y)                
                self.screen.blit(a.getImage(), (screenX, screenY, a.width, a.height))

                if(NAMES_ABOVE_AGENTS):
                    label = self.smallFont.render(a.getName(), 1, (0, 0, 0))
                    self.screen.blit(label, (screenX, screenY+TILE_HEIGHT))


    def drawAgents(self):
        for a in self.level.getAgents():
            projectedX = a.x-self.cameraX
            projectedY = a.y-self.cameraY

            if(self.isOnScreen(projectedX, projectedY)):
                (screenX, screenY) = self.tileCoordsToScreenCoords(a.x, a.y)

                self.screen.blit(a.getImage(), (screenX, screenY, a.width, a.height))

                if(NAMES_ABOVE_AGENTS):
                    label = self.smallFont.render(a.getName(), 1, (0, 0, 0))
                    self.screen.blit(label, (screenX, screenY+TILE_HEIGHT))

        
    def drawHealthBars(self):
        if(HEALTHBARS):
            for a in self.level.getAgents():
                (screenX, screenY) = self.tileCoordsToScreenCoords(a.x, a.y)
                
                pygame.draw.rect(self.screen,HEALTHBAR_OUTLINE_COLOUR,
                                 (screenX+(TILE_WIDTH-HEALTHBAR_WIDTH)/2.0,
                                  screenY-HEALTHBAR_FLOAT_AMOUNT,
                                  HEALTHBAR_WIDTH,HEALTHBAR_HEIGHT), 0)

                pygame.draw.rect(self.screen,HEALTHBAR_FILL_COLOUR,
                             (screenX+(TILE_WIDTH-HEALTHBAR_WIDTH)/2.0,
                              screenY-HEALTHBAR_FLOAT_AMOUNT,
                              HEALTHBAR_WIDTH*(a.fighter.getHealthPercent()/100.0),
                              HEALTHBAR_HEIGHT), 0)
    

    def handleCombatKeys(self):
        if(self.level.getPlayer().hasKnife):
            if(KNIFE_BUTTON in self.keysdown):
                self.keysdown.remove(KNIFE_BUTTON)
                self.level.getPlayer().startAttack()

    def handleLevelReset(self):
        if(DEBUG):
            if(RESET_BUTTON in self.keysdown):
                self.level.changeLevel(self.level.name)

    def handleLevelEditor(self):
        if(DEBUG):
            if(LEVEL_EDIT_BUTTON in self.keysdown):
                self.levelEditMode = not self.levelEditMode
                self.keysdown = []
                self.allTilesList = self.level.tileIdToTile.values()
                self.currentTileIndex = 0
                self.currentTileToPlace = self.allTilesList[self.currentTileIndex]



    def renderLighting(self):
        if(self.level.lightingOn):
            # regular ambient lighting
            filter = pygame.surface.Surface((GAME_WIDTH, GAME_HEIGHT))
            filter.fill(map(lambda x:255-x, self.level.ambientLight))


            # torch lighting
            for a in self.level.agents:
                if(a.torchOn):
                    (playerFaceX, playerFaceY) = a.faceTile()
                    playerX = a.x
                    playerY = a.y

                    deltaX = playerFaceX - playerX
                    deltaY = playerFaceY - playerY

                    torchX = playerX
                    torchY = playerY
                    lightingDone = False

                    while not lightingDone:
                        if(not self.level.canWalk(torchX, torchY, a)):
                            lightingDone = True
                        (screenX, screenY) = self.tileCoordsToScreenCoords(torchX, torchY)
                        pygame.draw.rect(filter, map(lambda x:255-x, a.torchLight),
                                         pygame.Rect(screenX, screenY,
                                                     TILE_WIDTH, TILE_HEIGHT), 0)            
                        torchX += deltaX
                        torchY += deltaY


            self.screen.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)


    def updateHaze(self):
        if(self.hazeTimer > 0):
            self.hazeTimer -= 1


    def renderHaze(self):
        if(self.hazeTimer > 0):
            self.hazeTimer -= 1
            haze = pygame.surface.Surface((GAME_WIDTH, GAME_HEIGHT))
            haze.fill(map(lambda x:255-x, self.hazeColour))
            self.screen.blit(haze, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        

    def drawLevelObjective(self):
        if(self.level.hasObjective):
            label = self.levelObjectiveFont.render(self.level.objective, 1, (255, 255, 255))
            self.screen.blit(label, (GAME_WIDTH-label.get_width(), 0))

    def runKnifeCombat(self):
        # a is the knifer
        for a in self.level.agents:
            if (a.currentlyKnifing):
                (faceX, faceY) = a.faceTile()

                # e is the person we are knifing
                e = self.level.agentAt(faceX, faceY)

                if(e != None):

                    # make the damage message appear underneath when
                    # we knife from above: otherwise hard to read
                    if a.facing == "down":
                        (screenX, screenY) = self.tileCoordsToScreenCoords(a.x, a.y)
                        screenX += TILE_WIDTH/2 - 4
                        screenY += DAMAGE_MESSAGE_FLOAT_DOWN_AMOUNT

                    else:
                        (screenX, screenY) = self.tileCoordsToScreenCoords(a.x, a.y)
                        screenX += TILE_WIDTH/2 - 4
                        screenY -= DAMAGE_MESSAGE_FLOAT_DOWN_AMOUNT


                    # check flanking, backstabbing etc.
                    (enemyFaceX, enemyFaceY) = e.faceTile()
                    deltaX = abs(enemyFaceX - a.x)
                    deltaY = abs(enemyFaceY - a.y)

                    # face to face
                    if(deltaX == 0 and deltaY == 0):
                        damageDealt = a.fighter.baseKnifeDamage
                        self.damageMessages.append((screenX, screenY,
                                                    "SHANK -" + str(damageDealt),
                                                    DAMAGE_MESSAGE_FRAMES,
                                                    SHANK_WIGGLE))
                        self.shakeScreen(SHANK_WIGGLE, DAMAGE_MESSAGE_FRAMES)

                    # back stab
                    elif((deltaX == 0 and deltaY == 2) or
                         (deltaX == 2 and deltaY == 0)):
                        damageDealt = a.fighter.baseKnifeDamage*BACKSTAB_BONUS
                        self.damageMessages.append((screenX, screenY,
                                                    "BACKSTAB -" + str(damageDealt),
                                                    DAMAGE_MESSAGE_FRAMES,
                                                    BACKSTAB_WIGGLE))
                        self.shakeScreen(BACKSTAB_WIGGLE, DAMAGE_MESSAGE_FRAMES)


                    # flanking
                    else:
                        damageDealt = a.fighter.baseKnifeDamage*FLANKING_BONUS
                        self.damageMessages.append((screenX, screenY,
                                                    "FLANK -" + str(damageDealt),
                                                    DAMAGE_MESSAGE_FRAMES,
                                                    FLANK_WIGGLE))
                        self.shakeScreen(FLANK_WIGGLE, DAMAGE_MESSAGE_FRAMES)


                        
                    e.dealDamage(damageDealt, a.x, a.y)

                    # red haze when we get hit
                    if(e == self.level.getPlayer()):
                        self.hazeScreen(DAMAGE_HAZE_COLOUR, 15)

                    a.currentlyKnifing = False


    def interactWithObjects(self):
        interactedWithThisFrame = ""
        (playerFaceX, playerFaceY) = self.level.getPlayer().faceTile()

        # check if player is facing any objects
        o = self.level.objectAt(playerFaceX, playerFaceY)
        if(o != None):
            self.displayPressEnterMessage(self.screen, self.smallFont, o)
            if (INTERACT_BUTTON in self.keysdown):
                m = Message(o.getDialogue(), (0, 0, 0), (255, 255, 255), self.messageFont)
                self.displayMessage(m, [""], self.smallFont)
                self.keysdown = []
                interactedWithThisFrame = o.getName()

        return interactedWithThisFrame
    
            
    def playOverworld(self, screen, clock, level, messageFont, smallFont, damageFont):
        self.cameraX = max(0, level.getPlayer().x - NUM_TILES_X/2)
        self.cameraY = max(0, level.getPlayer().y - NUM_TILES_Y/2)

        self.level = level
        self.screen = screen
        self.clock = clock
        
        self.levelObjectiveFont = smallFont
        self.damageMessageFont = damageFont
        self.messageFont = messageFont
        self.smallFont = smallFont

        self.clickPos = []
        self.scrollDowns = []
        self.scrollUps = []
        
        done = False
        
        while not done:
            self.clock.tick(FRAME_RATE)

            # handle events
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    self.keysdown.append(event.key)
                elif event.type == pygame.KEYUP:
                    if event.key in self.keysdown:
                        self.keysdown.remove(event.key)
                elif event.type == pygame.MOUSEBUTTONUP:
                    # scroll up
                    if event.button == 4:
                        self.scrollUps.append(1)
                    elif event.button == 5:
                        self.scrollDowns.append(1)
                    else:
                        self.clickPos.append(pygame.mouse.get_pos())

            ################################
            # handle key presses
            self.handleTorch()
            self.handleCombatKeys()
            self.handlePlayerMovement()
            self.handleLevelReset()
            self.handleLevelEditor()

            # run the agent AIs and update all agent frame counters
            self.runAI()

            # update display variables: camera, screen shake etc.
            self.updateCamera()
            self.updateScreenShake()
            self.updateHaze()

            ################################
            # render things
            # draw the background
            self.screen.fill(FILL_COLOUR)

            # pre lighting stuff
            self.renderLevelGrid()
            self.drawObjects()
            self.drawAgents()

            # lighting
            self.renderLighting()
            self.renderHaze()

            # post lighting (UI) stuff
            self.drawLevelObjective()
            self.drawDamageMessages()
            self.drawHealthBars()

            if(not self.levelEditMode):
                # combat, interactions etc.
                self.runKnifeCombat()
            
                interactedWithThisFrame = self.interactWithObjects()          


                pygame.display.flip()

                self.totalFrameCounter+=1

                # update agent list with newly dead agents
                nowDead = level.updateDeadAgents()

                self.level.checkActionTriggers(interactedWithThisFrame, self.totalFrameCounter, nowDead)

                # display any messages the level has for us
                for s in self.level.getMessages():
                    m = Message(s, (255, 0, 0), (255, 255, 255), messageFont)
                    self.displayMessage(m, [""], smallFont)
                    self.keysdown = []

                self.level.emptyMessages()


                # see if we can end the level
                if(self.level.readyForNextLevel):
                    return self.level.nextLevel

            else:
                # do the edit level mode stuff
                self.runLevelEditor()
                pygame.display.flip()
