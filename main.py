from settings import *
from sys import exit
from random import choice

#components
from game import Game
from score import Score
from preview_pieces import Preview

class Main:
    def __init__(self):

        # General
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()

        # shapes
        ## PIECE SORTER
        self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]

        # Components
        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score()
        self.preview = Preview()

    def update_score(self, lines, score, lvl):
        self.score.lines = lines
        self.score.score = score
        self.score.lvl = lvl

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(TETROMINOS.keys())))
        return next_shape

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.display_surface.fill('Gray')

            self.game.run()
            self.score.run()
            self.preview.run(self.next_shapes)

            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    main = Main()
    main.run()