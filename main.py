from settings import *
from sys import exit
from random import choice
from os.path import join
import csv

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

        #status
        self.state = 'menu'
        self.player_name = ''
        self.name_input_active = False

        self.font= pygame.font.Font(join('graphics', 'Russo_One.ttf'),40)
        # shapes
        ## PIECE SORTER
        self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]

        # Components
        self.score = Score()
        self.preview = Preview()
        self.init_game()

    def init_game(self):
        self.game = Game(self.get_next_shape, self.update_score)

    def update_score(self, lines, score, lvl):
        self.score.lines = lines
        self.score.score = score
        self.score.lvl = lvl

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(TETROMINOS.keys())))
        return next_shape

    def run(self):
        self.running = True
        while self.running:
            self.display_surface.fill('Gray')

            if self.state == 'menu':
                self.run_menu()
            elif self.state == 'enter_name':
                self.run_enter_name()
            elif self.state == 'game':
                self.run_game()
            elif self.state == 'game_over':
                self.run_game_over()
            elif self.state == 'high_scores':
                self.run_high_scores()

            pygame.display.update()
            self.clock.tick(60)

    def run_menu(self):
        self.draw_text("TETRIS", y=100)
        self.draw_text("Press ENTER to Start", y=200)
        self.draw_text("Press H for High Scores", y=260)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.init_game()
                    self.state = 'enter_name'
                    self.player_name = ''
                elif event.key == pygame.K_h:
                    self.state = 'high_scores'

    def run_enter_name(self):
        self.draw_text('Enter Your Name:', y=100)
        self.draw_text(self.player_name + "|", y=160)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.player_name.strip():
                    self.init_game()
                    self.state = 'game'
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    if len(self.player_name) < 12 and event.unicode.isprintable():
                        self.player_name += event.unicode

    def run_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


        self.game.run()
        self.score.run()
        self.preview.run(self.next_shapes)

        if self.game_over():
            self.save_score([self.player_name, self.score.score, self.score.lvl, self.score.lines])
            self.state = 'game_over'

    def run_game_over(self):
        self.draw_text('Game Over', y=150)
        self.draw_text("Press M for Menu", y=220)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.state = 'menu'

    def run_high_scores(self):
        self.draw_text("High Scores", y=50)
        self.draw_text('M for menu', y=WINDOW_HEIGHT - 60)

        try:
            with open('scoreboard.csv', 'r', newline='') as file:
                reader = list(csv.reader(file))

                valid_rows = [row for row in reader if len(row) == 4 and row[1].isdigit()]

                valid_rows.sort(key=lambda x: int(x[1]), reverse=True)

                for i, row in enumerate(valid_rows[:5]):
                    y = 120 + i * 50

                    # Background rectangle
                    rect_width = 500
                    rect_height = 40
                    rect_x = (WINDOW_WIDTH - rect_width) // 2
                    rect = pygame.Rect(rect_x, y - 20, rect_width, rect_height)
                    pygame.draw.rect(self.display_surface, '#333333', rect, border_radius=6)
                    pygame.draw.rect(self.display_surface, 'White', rect, 2, border_radius=6)

                    # Score text
                    score_text = f"{i + 1}. {row[0]} | Score: {row[1]} | Level: {row[2]} | Lines: {row[3]}"
                    self.draw_text(score_text, y=y)
        except FileNotFoundError:
            self.draw_text("No scores yet.", y=120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.state = 'menu'

    def draw_text(self, text, x=None, y=0):
        text_surf = self.font.render(text, True, 'White')
        rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2 if x is None else x, y))
        self.display_surface.blit(text_surf, rect)

    def save_score(self, score_data):
        with open('scoreboard.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(score_data)

    def game_over(self):
        # If the new tetromino starts overlapping existing blocks, it's game over
        for block in self.game.tetromino.blocks:
            x = int(block.pos.x)
            y = int(block.pos.y)
            if y >= 0 and self.game.field_data[y][x]:
                return True
        return False


if __name__ == "__main__":
    main = Main()
    main.run()

    main.save_score()