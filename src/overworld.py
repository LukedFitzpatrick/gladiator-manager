import pygame
from textrect import *
from constants import *


class Message:
    def __init__(self, text, colour, backgroundColour, font):
        self.text = text
        self.colour = colour
        self.backgroundColour = backgroundColour
        self.font = font  


# pops up a message and waits for key press        
def displayMessage(screen, message, clock, pressAnyKey=True):

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


    if(pressAnyKey):

        # display the 'press any key' 
        label = message.font.render("<press enter>", 1, PRESS_ANY_KEY_COLOUR)

        screen.blit(label, (GAME_WIDTH-PRESS_ANY_KEY_WIDTH-TEXT_PADDING_X,
                            GAME_HEIGHT-PRESS_ANY_KEY_HEIGHT-TEXT_PADDING_Y))

        pygame.display.flip()

        
        # wait for user to accept the message
        done = False
        while not done:
            clock.tick(FRAME_RATE)

            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:                   
                    # TODO cleanup the exit system
                    pygame.quit()

                elif event.type == pygame.KEYDOWN:
                    if(event.key == MESSAGE_ADVANCE_BUTTON):
                        done = True



# eventually pass level/scene objects into here
def playOverworld(screen, clock, level, messageFont):
    print "Playing overworld"

    # camera moves in tile coordinates
    cameraX = 0
    cameraY = 0

    keysdown = []
    
    frameCounter = 0
    
    done = False
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
        if(LEFT_BUTTON in keysdown):
            cameraX -= 1
            keysdown.remove(LEFT_BUTTON)

        if(RIGHT_BUTTON in keysdown):
            cameraX += 1
            keysdown.remove(RIGHT_BUTTON)

        if(UP_BUTTON in keysdown):
            cameraY -= 1
            keysdown.remove(UP_BUTTON)

        if(DOWN_BUTTON in keysdown):
            cameraY += 1
            keysdown.remove(DOWN_BUTTON)
                            

        # render
        screen.fill(FILL_COLOUR)
        
        # draw the level grid
        for x in range(cameraX, cameraX+NUM_TILES_X):
            for y in range(cameraY, cameraY+NUM_TILES_Y):
                screenX = (x-cameraX)*TILE_WIDTH
                screenY = (y-cameraY)*TILE_HEIGHT

                if(level.hasTile(x, y)):
                    t = level.getTile(x, y)
                    screen.blit(t.img, (screenX,screenY,TILE_WIDTH,TILE_HEIGHT))

                    # display hitboxes
                    if(HITBOXES and t.solid):
                        pygame.draw.rect(screen,(255,0,0),
                                     (screenX,screenY,TILE_WIDTH,TILE_HEIGHT), 1)

                # out of level hitboxes
                else:
                    if(HITBOXES):
                        pygame.draw.rect(screen,(0,0,255),
                                         (screenX,screenY,TILE_WIDTH,TILE_HEIGHT), 1)
  
                        
                        
        if(frameCounter % 100 == 0):
            m = Message("Hello, World! " + str(frameCounter), (0, 0, 0), (255, 255, 255), messageFont)
            displayMessage(screen, m, clock)

        pygame.display.flip()
        frameCounter+=1

