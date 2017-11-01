import pygame
from textrect import *
from constants import *
from agent import *


class Message:
    def __init__(self, text, colour, backgroundColour, font):
        self.text = text
        self.colour = colour
        self.backgroundColour = backgroundColour
        self.font = font  


# pops up a message and waits for key press        
def displayMessage(screen, message, clock, options, smallFont):


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


def conversation(screen, clock, messageFont, agent, smallFont):
    
    conversationState = "HELLO"

    while conversationState != "BYE":
        d = agent.getDialogue(conversationState)
        if(d == "GET_RECRUITED"):
            return "RECRUIT"
        if(d == "FIGHT"):
            return "FIGHT"
        else:
            m = Message(d, (0, 0, 0), (255, 255, 255), messageFont)
            conversationState = displayMessage(screen, m,  clock,
                                           ["TALK", "RECRUIT", "FIGHT", "BYE"],
                                           smallFont)
    return "BYE"
        


def displayPressEnterMessage(screen, font, o):
    label = font.render("<press enter>", 1, (255, 255, 255))
    screen.blit(label, (0, 0))


# eventually pass level/scene objects into here
def playOverworld(screen, clock, level, messageFont, smallFont):
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
                                        

                    

        
        (playerFaceX, playerFaceY) = level.getPlayer().faceTile()

        # check if the player is facing any agents
        a = level.agentAt(playerFaceX, playerFaceY)
        if(a != None):
            if (INTERACT_BUTTON in keysdown):
                displayPressEnterMessage(screen, o, smallFont)
                result = conversation(screen, clock, messageFont, a, smallFont)
                if(result == "RECRUIT"):
                    a.converser.setTree("ally")
                    level.getPlayer().addRecruit(a)
                keysdown = []

        # check if player is facing any objects
        o = level.objectAt(playerFaceX, playerFaceY)
        if(o != None):
            displayPressEnterMessage(screen, smallFont, o)
            if (INTERACT_BUTTON in keysdown):
                m = Message(o.getDialogue(), (0, 0, 0), (255, 255, 255), messageFont)
                displayMessage(screen, m, clock, [""], smallFont)
                keysdown = []

            
        pygame.display.flip()
        frameCounter+=1


    
