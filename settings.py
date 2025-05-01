from pickle import REDUCE

import pygame

# Game Size
COLUMNS = 10
ROWS = 20
CELL_SIZE = 40
GAME_HEIGHT = ROWS * CELL_SIZE
GAME_WIDTH = COLUMNS * CELL_SIZE

# Side Bar
SIDE_BAR_WIDTH = 200
PREVIEW_HEIGHT_FRACTION = 0.7
SCORE_HEIGHT_FRACTION = 1 - PREVIEW_HEIGHT_FRACTION

# window
PADDING = 20
WINDOW_WIDTH = GAME_WIDTH + SIDE_BAR_WIDTH + (PADDING * 3)
WINDOW_HEIGHT = GAME_HEIGHT + (PADDING * 2)

# Game Behavior
UPDATE_START_SPEED = 800
MOVE_WAIT_TIME = 200
ROTATE_WAIT_TIME = 200
BLOCK_OFFSET = pygame.Vector2(COLUMNS // 2, -1)

# Colors
Yellow = "#f1e60d"
Red = "#e51b20"
Blue = "#204b9b"
Green = "#65b32e"
Purple = "#7b217f"
Cyan = "#6cc6d9"
Orange = "#f07e13"
Gray = "#1C1C1C"