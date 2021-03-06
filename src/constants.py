import pygame

VERSION = "0.01"
DEBUG = True

TILE_WIDTH = 32
TILE_HEIGHT = 32
NUM_TILES_X = 12
NUM_TILES_Y = 12

OVERWORLD_HEIGHT = TILE_HEIGHT*NUM_TILES_Y
OVERWORLD_WIDTH = TILE_WIDTH*NUM_TILES_X


GAME_HEIGHT = OVERWORLD_HEIGHT
GAME_WIDTH = OVERWORLD_WIDTH

FRAME_RATE = 40

MOVE_LOCK_FRAMES = 1

MESSAGE_HEIGHT = TILE_HEIGHT*4
MESSAGE_WIDTH = OVERWORLD_WIDTH

TEXT_PADDING_X = 20
TEXT_PADDING_Y = 20


PRESS_ANY_KEY_X = 0
PRESS_ANY_KEY_HEIGHT = 15
PRESS_ANY_KEY_COLOUR = (100, 100, 100)

FILL_COLOUR = (0, 0, 0)


HITBOXES = False
NAMES_ABOVE_AGENTS = False

HEALTHBARS = True
HEALTHBAR_WIDTH = 16
HEALTHBAR_HEIGHT = 3
HEALTHBAR_OUTLINE_COLOUR = (255,0,0)
HEALTHBAR_FILL_COLOUR = (148, 224, 137)
HEALTHBAR_FLOAT_AMOUNT = HEALTHBAR_HEIGHT + 2


AI_STATUS_MARKS = True
AI_TARGET_BOXES = True

DAMAGE_MESSAGE_FRAMES = 15
DAMAGE_MESSAGE_COLOUR = (255,0,0)
DAMAGE_MESSAGE_FLOAT_AMOUNT = HEALTHBAR_FLOAT_AMOUNT + 20
DAMAGE_MESSAGE_FLOAT_DOWN_AMOUNT = TILE_HEIGHT + 5
SHANK_WIGGLE = 1
FLANK_WIGGLE = 4
BACKSTAB_WIGGLE = 8


LEFT_BUTTON = pygame.K_a
RIGHT_BUTTON = pygame.K_d
UP_BUTTON = pygame.K_w
DOWN_BUTTON = pygame.K_s

KNIFE_BUTTON = pygame.K_k

INTERACT_BUTTON = pygame.K_RETURN
ACCEPT_BUTTON = pygame.K_RETURN
RESET_BUTTON = pygame.K_r # only for debug?
TORCH_BUTTON = pygame.K_SPACE

LEVEL_EDIT_BUTTON = pygame.K_l
LEVEL_EDIT_SAVE_BUTTON = pygame.K_f

LEVEL_EDIT_MOVE_LEFT_BUTTON = pygame.K_LEFT
LEVEL_EDIT_MOVE_RIGHT_BUTTON = pygame.K_RIGHT
LEVEL_EDIT_MOVE_UP_BUTTON = pygame.K_UP
LEVEL_EDIT_MOVE_DOWN_BUTTON = pygame.K_DOWN


CAMERA_SLIDE_AMOUNT = 4
CAMERA_SLIDE_SPEED = 1

CAN_TURN_ON_THE_SPOT = True


AGENT_NAME_INDEX = 0
AGENT_X_INDEX = 1
AGENT_Y_INDEX = 2
AGENT_HEALTH_INDEX = 3
AGENT_KNIFE_DAMAGE_INDEX = 4
AGENT_UP_SPRITE_INDEX = 5
AGENT_DOWN_SPRITE_INDEX = 6
AGENT_LEFT_SPRITE_INDEX = 7
AGENT_RIGHT_SPRITE_INDEX = 8
AGENT_UP_KNIFE_SPRITE_INDEX = 9
AGENT_DOWN_KNIFE_SPRITE_INDEX = 10
AGENT_LEFT_KNIFE_SPRITE_INDEX = 11
AGENT_RIGHT_KNIFE_SPRITE_INDEX = 12
AGENT_TEAM_INDEX = 13
AGENT_AI_INDEX = 14
AGENT_FACING_INDEX = 15

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
ACTION_LANG_START_TORCH_ON = "startTorchOn"
ACTION_LANG_EVERY_N_FRAMES = "everyNFrames"
ACTION_LANG_GET_KNIFE = "getKnife"
ACTION_LANG_WHEN_AGENT_DIES = "whenAgentDies"
ACTION_LANG_WHEN_ONLY_PLAYER_SURVIVES = "whenOnlyPlayerSurvives"
ACTION_LANG_START_KNIFE = "startKnife"


TORCH_DECREMENT_PER_FRAME = 1
TORCH_INCREMENT_PER_MASH = 40

TORCH_BAR_WIDTH = 50
TORCH_BAR_HEIGHT = 10
TORCH_BAR_X = 5
TORCH_BAR_Y = GAME_HEIGHT - TORCH_BAR_HEIGHT - 5
TORCH_BAR_COLOUR = (191, 206, 114)


KNIFE_FRAMES = 5
BACKSTAB_BONUS = 8
FLANKING_BONUS = 2

AI_MOVE_DOWN = 0
AI_MOVE_UP = 1
AI_MOVE_LEFT = 2
AI_MOVE_RIGHT = 3
AI_KNIFE = 4
AI_NOTHING = 5

BUTTON_PRESS_SIMULATION_COOLDOWN = 2

AI_STATE_STAND_STILL = 0
AI_STATE_CLOSE_PATROL = 1
AI_STATE_KNIFE = 2
AI_STATE_WALK_FORWARD = 3
AI_STATE_MOVE_TOWARD = 4

TEAM_ALLY = 0
TEAM_EYE_CORPORATION = 1

GOON_AI_PLAN = 0
NO_AI_PLAN = 1


DAMAGE_HAZE_COLOUR = (200, 0, 0)

PLAYER_START_HEALTH = 10
PLAYER_KNIFE_DAMAGE = 1

CAMERA_SLIDE_ON = False



PCG_ROOM_WIDTH_MAX = 10
PCG_ROOM_WIDTH_MIN = 3
PCG_ROOM_HEIGHT_MAX = 10
PCG_ROOM_HEIGHT_MIN = 3

PCG_ROOMS_MIN = 10
PCG_ROOMS_MAX = 50

PCG_CORRIDOR_LENGTH_MIN = 1
PCG_CORRIDOR_LENGTH_MAX = 10

PCG_ROOM_MIN_ENEMIES = 0
PCG_ROOM_MAX_ENEMIES = 3

