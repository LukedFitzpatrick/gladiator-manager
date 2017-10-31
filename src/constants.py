import pygame

VERSION = "0.01"

TILE_WIDTH = 32
TILE_HEIGHT = 32
NUM_TILES_X = 16
NUM_TILES_Y = 16

OVERWORLD_HEIGHT = TILE_HEIGHT*NUM_TILES_Y
OVERWORLD_WIDTH = TILE_WIDTH*NUM_TILES_X
TEXT_HEIGHT = TILE_HEIGHT*4
TEXT_WIDTH = OVERWORLD_WIDTH

TEXT_PADDING_X = 20
TEXT_PADDING_Y = 20

GAME_HEIGHT = OVERWORLD_HEIGHT + TEXT_HEIGHT
GAME_WIDTH = OVERWORLD_WIDTH

FRAME_RATE = 30

