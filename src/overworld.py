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
        label = message.font.render("<press any key>", 1, PRESS_ANY_KEY_COLOUR)

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
                    done = True



# eventually pass level/scene objects into here
def playOverworld(screen, clock, messageFont):
    print "Playing overworld"

    i = 0
    
    done = False
    while not done:
        clock.tick(FRAME_RATE)
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                # todo clean up the exit system
                pygame.quit()
                return


        screen.fill((255, 255, 255))
        
        if(i % 100 == 0):
            m = Message("Hello, World! " + str(i), (0, 0, 0), (255, 255, 255), messageFont)
            displayMessage(screen, m, clock)

        pygame.display.flip()
        i+=1

