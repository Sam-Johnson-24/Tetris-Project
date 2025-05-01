import pygame.display
from settings import *

class Score:
    def __init__(self):
        self.surface = pygame.Surface((SIDE_BAR_WIDTH, (GAME_HEIGHT * SCORE_HEIGHT_FRACTION) - PADDING))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(bottomright = (WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))

    def run(self):
        self.display_surface.blit(self.surface, self.rect)