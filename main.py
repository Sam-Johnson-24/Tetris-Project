from settings import *
from sys import exit
from random import choice, shuffle
from os.path import join
import csv

#components
from game import Game
from score import Score
from preview_pieces import Preview

class Main:
    def __init__(self) -> None:
        """
        Initializes the main gameloop including core components.
        """

        # General
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()

        #status
        self.state = 'menu'
        self.player_name = ''
        self.name_input_active = False

        # Font
        self.font= pygame.font.Font(join('graphics', 'Russo_One.ttf'),40)

        # Piecebag
        self.next_shapes = []
        self.piecebag = []
        self.piecebag = list(TETROMINOS.keys())
        shuffle(self.piecebag)


        # Components
        self.score = Score()
        self.preview = Preview()
        self.init_game()

    def init_game(self) -> None:
        """
        Initializes the Game class instance as well as setting up the piecbag
        refreshing it if a game has already been played.
        """
        self.piecebag = []
        self.next_shapes = []

        self.refill_piecebag()
        self.refill_next_shapes()
        self.game = Game(self.get_next_shape, self.update_score)

    def update_score(self, lines, score, lvl) -> None:
        """
        Updates the lines, score and level variables of the game.

        :param lines (int): Number of lines cleared
        :param score (int): Point total from clearing lines
        :param lvl (int): relative speed based on cleared lines
        """
        self.score.lines = lines
        self.score.score = score
        self.score.lvl = lvl

    def refill_piecebag(self) -> None:
        """
        Refill the piecebag with a shuffled set of all tetromino types.
        """
        self.piecebag = list(TETROMINOS.keys())
        shuffle(self.piecebag)

    def refill_next_shapes(self) -> None:
        """
        Ensure there are always 3 shapes in the preview queue.
        """
        while len(self.next_shapes) < 3:
            if not self.piecebag:
                self.refill_piecebag()
            self.next_shapes.append(self.piecebag.pop())

    def get_next_shape(self) -> str:
        """
        Pop the next shape and refill preview queue.
        """
        if not self.next_shapes:
            self.refill_next_shapes()
        shape = self.next_shapes.pop(0)
        self.refill_next_shapes()
        return shape

    def run(self) -> None:
        """
        Controls screen selection and gamestate.
        """
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

    def run_menu(self) -> None:
        """
        Main menuloop.
        """
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

    def run_enter_name(self) -> None:
        """
        mainloop for starting a game; takes in player name.
        """
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

    def run_game(self) -> None:
        """
        mainloop for running game.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


        self.game.run()
        self.score.run()
        self.preview.run(self.next_shapes)

        if self.game_over():
            self.save_score([self.player_name, self.score.score, self.score.lvl, self.score.lines])
            self.state = 'game_over'

    def run_game_over(self) -> None:
        """
        Mainloop for game over state.
        """
        self.draw_text('Game Over', y=150)
        self.draw_text("Press M for Menu", y=220)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.state = 'menu'

    def run_high_scores(self) -> None:
        """
        Mainloop for scoreboard
        """
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
                    font = pygame.font.Font(join('graphics', 'Russo_One.ttf'),20)
                    self.draw_text(score_text, font=font, y=y)

        except FileNotFoundError:
            self.draw_text("No scores yet.", y=120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.state = 'menu'

    def draw_text(self, text: str, x: int = None, y: int = 0, font: pygame.font.Font = None) -> None:
        """
        Draws the text on the screen at the specified position.

        :param text (str): The text to be displayed.
        :param x (int, optional): The x-coordinate for the text position. Defaults to center.
        :param y (int, optional): The y-coordinate for the text position.
        :param font (pygame.font.Font, optional): The font to be used for rendering the text. Defaults to None.
        """
        if font is None:  # If no custom font is provided, use the default font
            font = self.font

        text_surf = font.render(text, True, 'White')
        rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2 if x is None else x, y))
        self.display_surface.blit(text_surf, rect)

    def save_score(self, score_data: tuple) -> None:
        """
        Sends post game data to scoreboard CSV
        """
        file_exists = os.path.exists('scoreboard.csv')
        write_header = not file_exists or os.path.getsize('scoreboard.csv') == 0
        with open('scoreboard.csv', 'a') as file:
            writer = csv.writer(file)
            if write_header:
                writer.writerow(['NAME', 'SCORE', 'LEVEL', 'LINES'])
            writer.writerow(score_data)

    def game_over(self) -> bool:
        """
        Checks for Game over condition
        """
        for block in self.game.tetromino.blocks:
            x = int(block.pos.x)
            y = int(block.pos.y)
            if y >= 0 and self.game.field_data[y][x]:
                return True
        return False


if __name__ == "__main__":
    main = Main()
    main.run()