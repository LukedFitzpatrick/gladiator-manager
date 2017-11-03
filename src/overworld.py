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


# pops up a message and waits for key press        
def displayMessage(screen, message, clock, options, smallFont, level):


    currentOptionIndex = 0
    

    # wait for user to accept the message
    done = False
    while not done:
        clock.tick(FRAME_RATE)
        # display the message box
        pygame.draw.rect(screen, (255,255,255),(0,GAME_HEIGHT-MESSAGE_HEIGHT,MESSAGE_WIDTH,MESSAGE_HEIGHT), 0)

        pygame.draw.rect(screen, (100,100,100),(0,GAME_HEIGHT-MESSAGE_HEIGHT,MESSAGE_WIDTH,MESSAGE_HEIGHT), 10)
        pygame.draw.rect(screen, (0,0,0),(0,GAME_HEIGHT-MESSAGE_HEIGHT,MESSAGE_WIDTH,MESSAGE_HEIGHT), 5)

        # word wrap the message into a label
        messageRect = pygame.Rect(TEXT_PADDING_X, OVERWORLD_HEIGHT+TEXT_PADDING_Y,
                              MESSAGE_WIDTH-(TEXT_PADDING_X*2), MESSAGE_HEIGHT-(TEXT_PADDING_Y*2))
    
        label = render_textrect(message.text, message.font, messageRect,
                            message.colour, message.backgroundColour, 0)
    
        screen.blit(label, (TEXT_PADDING_X, (OVERWORLD_HEIGHT-MESSAGE_HEIGHT)+TEXT_PADDING_Y))
        pygame.display.flip()

        
        optionsMessage = options[currentOptionIndex]

        
        optionText = options[currentOptionIndex]
        if(currentOptionIndex > 0):
            optionText = "<- " + optionText
        if(currentOptionIndex < len(options)-1):
            optionText += " ->"
            
        label = smallFont.render(optionText, 1, PRESS_ANY_KEY_COLOUR)
        
        screen.blit(label, (PRESS_ANY_KEY_X+TEXT_PADDING_X,
                        GAME_HEIGHT-PRESS_ANY_KEY_HEIGHT-TEXT_PADDING_Y))

        pygame.display.flip()


        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:                   
                # TODO cleanup the exit system
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if(event.key == ACCEPT_BUTTON):
                    return options[currentOptionIndex]

                elif(event.key == RIGHT_BUTTON):
                    currentOptionIndex = (currentOptionIndex+1) % len(options)

                elif(event.key == LEFT_BUTTON):
                    currentOptionIndex = (currentOptionIndex-1) % len(options)



def isOnScreen(x, y):
    return (x >= 0 and x <= NUM_TILES_X and y >= 0 and y <= NUM_TILES_Y)
        


def displayPressEnterMessage(screen, font, o):
    label = font.render("<press enter>", 1, (255, 255, 255))
    screen.blit(label, (0, 0))

def displayObjective(screen, font, objective):
    label = font.render(objective, 1, (255, 255, 255))

    screen.blit(label, (GAME_WIDTH-label.get_width(), 0))

def drawTorchBar(screen, torchPercent, font):
    # the outline
    pygame.draw.rect(screen,(255,255,255),
                     (TORCH_BAR_X,TORCH_BAR_Y,TORCH_BAR_WIDTH,TORCH_BAR_HEIGHT), 2)

    # the fill
    pygame.draw.rect(screen, TORCH_BAR_COLOUR,
                     (TORCH_BAR_X, TORCH_BAR_Y,
                      TORCH_BAR_WIDTH*(torchPercent/100.0),TORCH_BAR_HEIGHT), 0)
                    


def drawDamageMessages(screen, damageMessages, font):
    remainingMessages = []
    for d in damageMessages:
        (screenX, screenY, damage, framesLeft) = d
        label = font.render("-"+str(damage), 1, DAMAGE_MESSAGE_COLOUR)
        screen.blit(label, (screenX, screenY))

        if framesLeft > 1:
            remainingMessages.append(
                (screenX+randint(-DAMAGE_MESSAGE_WIGGLE,DAMAGE_MESSAGE_WIGGLE),
                 screenY-1,
                 damage,
                 framesLeft-1))

    return remainingMessages
    

# eventually pass level/scene objects into here
def playOverworld(screen, clock, level, messageFont, smallFont, damageFont):
    print "Playing overworld"

    # camera moves in tile coordinates
    cameraX = level.getPlayer().x - NUM_TILES_X/2
    cameraY = level.getPlayer().y - NUM_TILES_Y/2


    keysdown = []
    
    frameCounter = 0
    moveLock = 0
    
    done = False

    cameraSlideXPixels = 0
    cameraSlideYPixels = 0

    light = pygame.image.load("data/circle.png")


    damageMessages = []
    
    while not done:
        clock.tick(FRAME_RATE)
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                # todo clean up the exit system
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                keysdown.append(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in keysdown:
                    keysdown.remove(event.key)                


        # handle torch charging
        if(level.torchOn and TORCH_BUTTON in keysdown):
            keysdown.remove(TORCH_BUTTON)
            level.chargeTorch(TORCH_INCREMENT_PER_MASH)
                    
        # handle key presses
        if (moveLock == 0):
            if(LEFT_BUTTON in keysdown):
                level.getPlayer().translate(-1, 0, level)
                moveLock = MOVE_LOCK_FRAMES

            elif(RIGHT_BUTTON in keysdown):
                level.getPlayer().translate(1, 0, level)
                moveLock = MOVE_LOCK_FRAMES

            elif(UP_BUTTON in keysdown):
                level.getPlayer().translate(0, -1, level)
                moveLock = MOVE_LOCK_FRAMES

            elif(DOWN_BUTTON in keysdown):
                level.getPlayer().translate(0, 1, level)
                moveLock = MOVE_LOCK_FRAMES
        else:
            moveLock = max(moveLock-1, 0)

        # run the agent AI/ updating frames
        for a in level.agents:
            a.updateFrames()
            if(a != level.getPlayer()):
                move = a.runAI(level)
                if(move == AI_MOVE_DOWN):
                    a.translate(0, 1, level)
                elif(move == AI_MOVE_UP):
                    a.translate(0, -1, level)
                elif(move == AI_MOVE_LEFT):
                    a.translate(-1, 0, level)
                elif(move == AI_MOVE_RIGHT):
                    a.translate(1, 0, level)
                elif(move == AI_KNIFE):
                    a.startAttack()
            
        # make the camera follow the player
        oldCameraX = cameraX
        cameraX = level.getPlayer().x - NUM_TILES_X/2
        oldCameraY = cameraY
        cameraY = level.getPlayer().y - NUM_TILES_Y/2

        
        if(cameraX > oldCameraX):
            cameraSlideXPixels += CAMERA_SLIDE_AMOUNT
        elif(cameraX < oldCameraX):
            cameraSlideXPixels -= CAMERA_SLIDE_AMOUNT
        if(cameraY > oldCameraY):
            cameraSlideYPixels += CAMERA_SLIDE_AMOUNT
        elif(cameraY < oldCameraY):
            cameraSlideYPixels -= CAMERA_SLIDE_AMOUNT

        if(cameraSlideXPixels < -CAMERA_SLIDE_SPEED):
            cameraSlideXPixels += CAMERA_SLIDE_SPEED
        elif(cameraSlideXPixels > CAMERA_SLIDE_SPEED):
            cameraSlideXPixels -= CAMERA_SLIDE_SPEED
        if(cameraSlideYPixels < -CAMERA_SLIDE_SPEED):
            cameraSlideYPixels += CAMERA_SLIDE_SPEED
        elif(cameraSlideYPixels > CAMERA_SLIDE_SPEED):
            cameraSlideYPixels -= CAMERA_SLIDE_SPEED


            
        # render
        screen.fill(FILL_COLOUR)


        
        # draw the level grid
        for x in range(cameraX-1, cameraX+NUM_TILES_X+1):
            for y in range(cameraY-1, cameraY+NUM_TILES_Y+1):
                screenX = (x-cameraX)*TILE_WIDTH + cameraSlideXPixels
                screenY = (y-cameraY)*TILE_HEIGHT + cameraSlideYPixels

                # draw tiles
                if(level.hasTile(x, y)):
                    t = level.getTile(x, y)
                    screen.blit(t.getImage(), (screenX,screenY,TILE_WIDTH,TILE_HEIGHT))

                    # display hitboxes
                    if(HITBOXES and t.solid):
                        pygame.draw.rect(screen,(255,0,0),
                                     (screenX,screenY,TILE_WIDTH,TILE_HEIGHT), 1)

                # out of level hitboxes
                else:
                    if(HITBOXES):
                        pygame.draw.rect(screen,(0,0,255),
                                         (screenX,screenY,TILE_WIDTH,TILE_HEIGHT), 1)


        # now draw the objects
        for a in level.getObjects():
            projectedX = a.x-cameraX
            projectedY = a.y-cameraY

            if(isOnScreen(projectedX, projectedY)):
                screenX = projectedX*TILE_WIDTH + cameraSlideXPixels
                screenY = projectedY*TILE_HEIGHT + cameraSlideYPixels
                
                screen.blit(a.getImage(), (screenX, screenY, a.width, a.height))

                if(NAMES_ABOVE_AGENTS):
                    label = smallFont.render(a.getName(), 1, (0, 0, 0))
                    screen.blit(label, (screenX, screenY+TILE_HEIGHT))


        # now draw the agents
        for a in level.getAgents():
            projectedX = a.x-cameraX
            projectedY = a.y-cameraY

            if(isOnScreen(projectedX, projectedY)):
                screenX = projectedX*TILE_WIDTH + cameraSlideXPixels
                screenY = projectedY*TILE_HEIGHT + cameraSlideYPixels
                
                screen.blit(a.getImage(), (screenX, screenY, a.width, a.height))

                if(NAMES_ABOVE_AGENTS):
                    label = smallFont.render(a.getName(), 1, (0, 0, 0))
                    screen.blit(label, (screenX, screenY+TILE_HEIGHT))

                if(HEALTHBARS):
                    pygame.draw.rect(screen,HEALTHBAR_OUTLINE_COLOUR,
                                     (screenX+(TILE_WIDTH-HEALTHBAR_WIDTH)/2.0,
                                      screenY-HEALTHBAR_FLOAT_AMOUNT,
                                      HEALTHBAR_WIDTH,HEALTHBAR_HEIGHT), 0)

                    pygame.draw.rect(screen,HEALTHBAR_FILL_COLOUR,
                                     (screenX+(TILE_WIDTH-HEALTHBAR_WIDTH)/2.0,
                                      screenY-HEALTHBAR_FLOAT_AMOUNT,
                                      HEALTHBAR_WIDTH*(a.fighter.getHealthPercent()/100.0),
                                      HEALTHBAR_HEIGHT), 0)

                    
        # combat! Knifing
        if(level.getPlayer().hasKnife):
            if(KNIFE_BUTTON in keysdown):
                keysdown.remove(KNIFE_BUTTON)
                level.getPlayer().startAttack()

        # do lighting/torch lighting
        if(level.lightingOn):
            filter = pygame.surface.Surface((GAME_WIDTH, GAME_HEIGHT))
            filter.fill(map(lambda x:255-x, level.ambientLight))

            (playerFaceX, playerFaceY) = level.getPlayer().faceTile()
            playerX = level.getPlayer().x
            playerY = level.getPlayer().y

            deltaX = playerFaceX - playerX
            deltaY = playerFaceY - playerY

            if(level.torchOn and level.needTorchLighting()):
                torchX = playerX
                torchY = playerY
                lightingDone = False

                while not lightingDone:
                    if(not level.canWalk(torchX, torchY, level.getPlayer())):
                       lightingDone = True
                    screenX = (torchX-cameraX)*TILE_WIDTH + cameraSlideXPixels
                    screenY = (torchY-cameraY)*TILE_HEIGHT + cameraSlideYPixels
                    pygame.draw.rect(filter, map(lambda x:255-x, level.getTorchLight()),
                                     pygame.Rect(screenX, screenY,
                                                 TILE_WIDTH, TILE_HEIGHT), 0)            
                    torchX += deltaX
                    torchY += deltaY

                level.chargeTorch(-TORCH_DECREMENT_PER_FRAME)
                
            screen.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
                    
        if(level.torchOn):
            drawTorchBar(screen, level.getTorchPercentage(), smallFont)

        # drawing objective has to go after lighting
        if(level.hasObjective):
            displayObjective(screen, smallFont, level.objective)

        damageMessages = drawDamageMessages(screen, damageMessages, damageFont)

            

        interactedWithThisFrame = ""



        # check knife damage
        for a in level.agents:
            if (a.currentlyKnifing):
                (faceX, faceY) = a.faceTile()
                e = level.agentAt(faceX, faceY)

                if(e != None):
                    # todo make more elaborate

                    # check flanking etc.
                    (enemyFaceX, enemyFaceY) = e.faceTile()
                    deltaX = abs(enemyFaceX - a.x)
                    deltaY = abs(enemyFaceY - a.y)
                    print str(deltaX) + " " + str(deltaY)

                    
                    # face to face
                    if(deltaX == 0 and deltaY == 0):
                        damageDealt = a.fighter.baseKnifeDamage

                    # back stab
                    elif((deltaX == 0 and deltaY == 2) or
                         (deltaX == 2 and deltaY == 0)):
                        damageDealt = a.fighter.baseKnifeDamage*BACKSTAB_BONUS

                    # flanking
                    else:
                        damageDealt = a.fighter.baseKnifeDamage*FLANKING_BONUS
                        
                    e.fighter.dealDamage(damageDealt)

                    screenX = (a.x-cameraX)*TILE_WIDTH + cameraSlideXPixels + TILE_WIDTH/2-4
                    if a.facing == "down":
                        screenY = (a.y-cameraY)*TILE_HEIGHT+cameraSlideYPixels+DAMAGE_MESSAGE_FLOAT_DOWN_AMOUNT
                    else:
                        screenY = (a.y-cameraY)*TILE_HEIGHT+cameraSlideYPixels-DAMAGE_MESSAGE_FLOAT_AMOUNT

                    damageMessages.append((screenX, screenY, damageDealt, DAMAGE_MESSAGE_FRAMES))
                    a.currentlyKnifing = False

        

        # check if the player is facing any agents so we can interact with them
        (playerFaceX, playerFaceY) = level.getPlayer().faceTile()
        a = level.agentAt(playerFaceX, playerFaceY)
        if(a != None):
            if (INTERACT_BUTTON in keysdown):
                displayPressEnterMessage(screen, o, smallFont)
                #result = conversation(screen, clock, messageFont, a, smallFont)
                interactedWithThisFrame = a.getName()
                keysdown = []

        # check if player is facing any objects
        o = level.objectAt(playerFaceX, playerFaceY)
        if(o != None):
            displayPressEnterMessage(screen, smallFont, o)
            if (INTERACT_BUTTON in keysdown):
                m = Message(o.getDialogue(), (0, 0, 0), (255, 255, 255), messageFont)
                displayMessage(screen, m, clock, [""], smallFont, level)
                keysdown = []
                interactedWithThisFrame = o.getName()



        
        pygame.display.flip()

        frameCounter+=1

        stillAlive = []
        nowDead = []
        # check for deaths
        for a in level.agents:
            if (not a.fighter.alive):
                nowDead.append(a)
            else:
                stillAlive.append(a)

        level.agents = stillAlive

        # TODO pass now dead to check action triggers eventually
        # trigger any actions
        level.checkActionTriggers(interactedWithThisFrame, frameCounter)

        # check if the level has any messages for us
        for s in level.getMessages():
            m = Message(s, (255, 0, 0), (255, 255, 255), messageFont)
            displayMessage(screen, m, clock, [""], smallFont, level)
            keysdown = []

        level.emptyMessages()

        
        # see if we can end the level
        if(level.readyForNextLevel):
            return level.nextLevel

