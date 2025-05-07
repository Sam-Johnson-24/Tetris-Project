import pygame.display
from settings import *
from os.path import join

class Score:
    def __init__(self):
        self.surface = pygame.Surface((SIDE_BAR_WIDTH, (GAME_HEIGHT * SCORE_HEIGHT_FRACTION) - PADDING))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(bottomright = (WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))

        #font
        self.font = pygame.font.Font(join('graphics', 'Russo_One.ttf'),50)

        #display
        self.increment_height = self.surface.get_height() / 3

        #data
        self.score = 0
        self.lvl = 1
        self.lines = 0

    def display_text(self, pos, text):
        text_surface = self.font.render(f'{text[0]}:{text[1]}', True, 'White')
        text_rect = text_surface.get_rect(center= pos)
        self.surface.blit(text_surface, text_rect)

    def run(self):
        self.surface.fill('Gray')
        for i, text in enumerate([('Score', self.score), ('Level', self.lvl), ('Lines', self.lines)]):
            x = self.surface.get_width() / 2
            y = self.increment_height / 2 + (i * self.increment_height)
            self.display_text((x,y), text)

        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, 'White', self.rect, 2, 2)