import pygame
from textrect import *
from constants import *


class Message:
    def __init__(self, text, colour, backgroundColour, font):
        self.text = text
        self.colour = colour
        self.backgroundColour = backgroundColour
        self.font = font

        
    


def displayMessage(screen, message):

    # display the message box
    pygame.draw.rect(screen, (100,100,100),(0,OVERWORLD_HEIGHT,TEXT_WIDTH,TEXT_HEIGHT), 10)
    pygame.draw.rect(screen, (0,0,0),(0,OVERWORLD_HEIGHT,TEXT_WIDTH,TEXT_HEIGHT), 5)

    # word wrap the message into a label
    messageRect = pygame.Rect(TEXT_PADDING_X, OVERWORLD_HEIGHT+TEXT_PADDING_Y,
                   TEXT_WIDTH-(TEXT_PADDING_X*2), TEXT_HEIGHT-(TEXT_PADDING_Y*2))
    
    label = render_textrect(message.text, message.font, messageRect,
                            message.colour, message.backgroundColour, 0)
    
    #label = messageFont.render(message.text, 1, message.colour)
    screen.blit(label, (TEXT_PADDING_X, OVERWORLD_HEIGHT+TEXT_PADDING_Y))
    


# eventually pass level/scene objects into here
def playOverworld(screen, clock, messageFont):
    print "Playing overworld"

    done = False
    while not done:
        clock.tick(FRAME_RATE)
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        m = Message("Hello, World!", (0, 0, 0), (255, 255, 255), messageFont)

        screen.fill((255, 255, 255))
        displayMessage(screen, m)
        pygame.display.flip()
        
