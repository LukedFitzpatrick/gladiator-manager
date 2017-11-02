import pygame

VERSION = "0.01"

TILE_WIDTH = 32
TILE_HEIGHT = 32
NUM_TILES_X = 12
NUM_TILES_Y = 12

OVERWORLD_HEIGHT = TILE_HEIGHT*NUM_TILES_Y
OVERWORLD_WIDTH = TILE_WIDTH*NUM_TILES_X


GAME_HEIGHT = OVERWORLD_HEIGHT
GAME_WIDTH = OVERWORLD_WIDTH

FRAME_RATE = 30

MOVE_LOCK_FRAMES = 2

MESSAGE_HEIGHT = TILE_HEIGHT*4
MESSAGE_WIDTH = OVERWORLD_WIDTH

TEXT_PADDING_X = 20
TEXT_PADDING_Y = 20


PRESS_ANY_KEY_X = 0
PRESS_ANY_KEY_HEIGHT = 15
PRESS_ANY_KEY_COLOUR = (100, 100, 100)

FILL_COLOUR = (0, 0, 0)#(255, 255, 255)


HITBOXES = False
NAMES_ABOVE_AGENTS = False


LEFT_BUTTON = pygame.K_a
RIGHT_BUTTON = pygame.K_d
UP_BUTTON = pygame.K_w
DOWN_BUTTON = pygame.K_s

INTERACT_BUTTON = pygame.K_RETURN
ACCEPT_BUTTON = pygame.K_RETURN

TORCH_BUTTON = pygame.K_SPACE

CAMERA_SLIDE_AMOUNT = 4
CAMERA_SLIDE_SPEED = 1

CAN_TURN_ON_THE_SPOT = True


AGENT_NAME_INDEX = 0
AGENT_X_INDEX = 1
AGENT_Y_INDEX = 2
AGENT_UP_SPRITE_INDEX = 3
AGENT_DOWN_SPRITE_INDEX = 4
AGENT_LEFT_SPRITE_INDEX = 5
AGENT_RIGHT_SPRITE_INDEX = 6
AGENT_CONVERSER_INDEX = 7


TILE_ID_INDEX = 0
TILE_IMAGE_PATH_INDEX = 1
TILE_SOLID_INDEX = 2


OBJECT_NAME_INDEX = 0
OBJECT_X_INDEX = 1
OBJECT_Y_INDEX = 2
OBJECT_SPRITE_INDEX = 3
OBJECT_DIALOGUE_INDEX = 4


ACTION_LANG_INITIAL_STATE = "startState"
ACTION_LANG_BEGIN_ACTION = "begin"
ACTION_LANG_END_ACTION = "end"
ACTION_LANG_WHEN_IN_STATE = "whenInState"
ACTION_LANG_WHEN_INTERACT_WITH = "whenInteractWith"
ACTION_LANG_CHANGE_STATE_TO = "changeStateTo"
ACTION_LANG_MESSAGE = "message"
ACTION_LANG_CHANGE_OBJECT_TILE = "changeObjectTile"
ACTION_LANG_CHANGE_OBJECT_DIALOGUE = "changeObjectDialogue"
ACTION_LANG_CHANGE_LEVEL = "changeLevel"
ACTION_LANG_OBJECTIVE = "objective"
ACTION_LANG_START_LIGHT = "startLight"
ACTION_LANG_INVERT_LIGHTING = "invertLighting"
ACTION_LANG_START_LIGHT_STATE = "startLightState"
ACTION_LANG_CHANGE_LIGHT_STATE = "changeLightStateTo"
ACTION_LANG_SET_LIGHT = "setLight"
ACTION_LANG_WHEN_IN_LIGHT_STATE = "whenInLightState"
ACTION_LANG_GET_TORCH = "getTorch"
ACTION_LANG_START_TORCH_LIGHT = "startTorchLight"
ACTION_LANG_START_TORCH = "startTorch"


TORCH_DECREMENT_PER_FRAME = 1
TORCH_INCREMENT_PER_MASH = 40

TORCH_BAR_WIDTH = 50
TORCH_BAR_HEIGHT = 10
TORCH_BAR_X = 5
TORCH_BAR_Y = GAME_HEIGHT - TORCH_BAR_HEIGHT - 5
TORCH_BAR_COLOUR = (191, 206, 114)
