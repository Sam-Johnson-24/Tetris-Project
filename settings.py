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
UPDATE_START_SPEED = 500

MOVE_WAIT_TIME = 100
ROTATE_WAIT_TIME = 100
BLOCK_OFFSET = pygame.Vector2(COLUMNS // 2, -2)

# Colors
Yellow = "#f1e60d"
Red = "#e51b20"
Blue = "#204b9b"
Green = "#65b32e"
Purple = "#7b217f"
Cyan = "#6cc6d9"
Orange = "#f07e13"
Gray = "#1C1C1C"

# Shapes
TETROMINOS = {
    'T': {'shape': [(0,0), (-1,0), (1,0), (0,-1)], 'color': Purple},
    'O': {'shape': [(0,0), (1,0), (1,1), (0,1)], 'color': Yellow},
    'J': {'shape': [(0,0), (0,-1), (0,1), (-1,1)], 'color': Blue},
    'L': {'shape': [(0,0), (0,-1), (0,1), (1,1)], 'color': Orange},
    'I': {'shape': [(0,0), (0,1), (0,2), (0,-1)], 'color': Cyan},
    'S': {'shape': [(0,0), (1,0), (0,1), (-1,1)], 'color': Green},
    'Z': {'shape': [(0,0), (-1,0), (0,1), (1,1)], 'color': Red}
}

SCORE_DATA = {1: 40, 2: 100, 3: 300, 4: 1200}