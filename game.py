from pydoc import browse
from symtable import Class

from settings import *
from random import choice
from timer import Timer


class Game:
    def __init__(self, get_next_shape, update_score) -> None:
        """
        Initializes class variables and board-state
        """

        # General Settings
        self.surface = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (PADDING, PADDING))
        self.sprites = pygame.sprite.Group()

        # game connections
        self.get_next_shape = get_next_shape
        self.update_score = update_score

        # Lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0,255,0))
        self.line_surface.set_colorkey((0,255,0))
        self.line_surface.set_alpha(120)

        # tetromino
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        ## PIECE SORTER NEEDED
        self.tetromino = Tetromino(choice(list(TETROMINOS.keys())),
                                   self.sprites,
                                   self.create_new_tetromino,
                                   self.field_data)

        # timer
        self.down_speed = UPDATE_START_SPEED
        self.down_speed_faster = self.down_speed * 0.3
        self.down_pressed = False

        self.timers = {
            'vertical move': Timer(self.down_speed, True, self.move_down),
            'horizontal move': Timer(MOVE_WAIT_TIME),
            'rotation move': Timer(ROTATE_WAIT_TIME)
        }
        self.timers['vertical move'].activate()

        #score
        self.current_lvl = 1
        self.current_score = 0
        self.current_lines = 0

    def calc_score(self, num_lines) -> None:
        """
        Updates score variables when lines are cleared

        :param num_lines (int): number of lines to use for updates
        """
        self.current_lines += num_lines
        self.current_score += SCORE_DATA[num_lines] * self.current_lvl

        if self.current_lines / 10 > self.current_lvl:
            self.current_lvl += 1
            self.down_speed *= 0.80
            self.down_speed_faster = self.down_speed * 0.3
            self.timers['vertical move'].duration = self.down_speed

        self.update_score(self.current_lines, self.current_score, self.current_lvl)

    def create_new_tetromino(self) -> None:
        """
        Creates new instance of tetromino and changes player control to it
        """

        self.check_finished_rows()
        new_tetromino = Tetromino(self.get_next_shape(), self.sprites, self.create_new_tetromino, self.field_data)

        # Check for overlap at spawn
        for block in new_tetromino.blocks:
            x = int(block.pos.x)
            y = int(block.pos.y)
            if y >= 0 and self.field_data[y][x]:
                self.tetromino = new_tetromino
                return

        self.tetromino = new_tetromino

    def timer_update(self) -> None:
        """
        Global timer updates
        """
        for timer in self.timers.values():
            timer.update()

    def move_down(self) -> None:
        """
        Moves player tetromino down
        """
        self.tetromino.move_down()

    def draw_grid(self) -> None:
        """Draws Game board"""

        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.surface,"White", (x,0), (x,self.surface.get_height()), 1)

        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.surface, "White", (0,y), (self.surface.get_width(), y), 1)

        self.surface.blit(self.line_surface, (0,0))

    def input(self) -> None:
        """
        Handles player input on arrow keys
        """
        keys = pygame.key.get_pressed()

        if not self.timers['horizontal move'].active:

            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activate()

            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move'].activate()

        if not self.timers['rotation move'].active:
            if keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers['rotation move'].activate()

        #down speedup
        if not self.down_pressed and keys[pygame.K_DOWN]:
            self.down_pressed = True
            self.timers['vertical move'].duration = self.down_speed_faster

        if self.down_pressed and not keys[pygame.K_DOWN]:
            self.down_pressed = False
            self.timers['vertical move'].duration = self.down_speed

    def check_finished_rows(self) -> None:
        """
        Handles deletion of completed rows and related board updates
        """

        # get full row indexs
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(i)

        if delete_rows:
            for delete_row in delete_rows:

                # delete full row
                for block in self.field_data[delete_row]:
                    block.kill()

                # move down blocks
                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1
            #rebuild field_data
            self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

            self.calc_score(len(delete_rows))

    def run(self) -> None:
        """
        Runs Game mainloop
        """

        # update
        self.input()
        self.timer_update()
        self.sprites.update()
        # Drawing
        self.surface.fill(Gray)
        self.sprites.draw(self.surface)

        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING,PADDING))
        pygame.draw.rect(self.display_surface, 'White', self.rect, 2, 2)

class Tetromino:
    def __init__(self, shape: str, group: any, create_new_tetromino: callable, field_data: list) -> None:
        """
        Initializes a new tetromino

        :param shape: The shape of the tetromino
        :param group: Container for the individual blocks
        :param create_new_tetromino: Callback function to create a new tetromino
        :param field_data: Current board state for checking collision
        """
        # Setup
        self.shape = shape
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data

        # create blocks
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

    # Collisions
    def next_move_horizontal_collide(self, blocks: list, amount: int) -> bool:
        """
        Collects the location of each block in active tetromino for checking horizontal collision
        :param blocks: list of tuples containing coordinates of each block
        :param amount: direction of movement
        :return: returns True if collision occurs otherwise returns true
        """
        collision_list = [block.horizontal_collide(int(block.pos.x) + amount, self.field_data) for block in self.blocks]
        return True if any(collision_list) else False

    def next_move_vertical_collide(self, blocks, amount) -> bool:
        """
        Collects the location of each block in active tetromino for checking vertical collision
        :param blocks: list of tuples containing coordinates of each block
        :param amount: direction of movement
        :return: returns True if collision occurs otherwise returns true
        """
        collision_list = [block.vertical_collide(int(block.pos.y) + amount, self.field_data) for block in self.blocks]
        return True if any(collision_list) else False

    # Movement
    def move_horizontal(self, amount) -> None:
        """
        Moves the active tetromino left or right
        :param amount: direction of move
        """
        if not self.next_move_horizontal_collide(self.blocks, amount):
            for block in self.blocks:
                block.pos.x += amount

    def move_down(self) -> None:
        """
        Moves the active tetromino down or makes a new one if unable to
        """
        if not self.next_move_vertical_collide(self.blocks, 1):
            for block in self.blocks:
                block.pos.y += 1
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.create_new_tetromino()

    def rotate(self) -> None:
        """
        Spins the active tetromino in place 90 degrees clockwise, excepting "O" blocks
        """
        if self.shape != 'O':
            pivot_pos = self.blocks[0].pos
            new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

            # collision
            for pos in new_block_positions:
                # horizontal
                if pos.x < 0 or pos.x >= COLUMNS:
                    return
                # field
                if self.field_data[int(pos.y)][int(pos.x)]:
                    return
                # vert/floor check
                if pos.y > ROWS:
                    return

            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]

class Block(pygame.sprite.Sprite):
    def __init__(self, group: any, pos: tuple, color: str) -> None:
        """
        Initializes a new block
        :param group: Group location for the block
        :param pos: tuple containing the coords for the block
        :param color: string containing the color id from the settings file
        """

        # General
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE,CELL_SIZE))
        self.image.fill(color)

        # position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft = self.pos * CELL_SIZE)

    def rotate(self, pivot_pos: tuple) -> tuple:
        """
        Takes the location of a block and moves it to the new position after applying a rotation
        :param pivot_pos: tuple of the current location
        :return: tuple of the rotated position
        """
        return pivot_pos + (self.pos - pivot_pos).rotate(90)

    def horizontal_collide(self, x, field_data) -> bool:
        """
        returns True if the block would collide with the board edge or the side of another block
        :param x: x coord on the game board
        :param field_data: current boardstate of the whole field
        :return: True if collision occurs, otherwise returns nothing
        """
        if not 0 <= x < COLUMNS:
            return True

        if field_data[int(self.pos.y)][x]:
            return True

    def vertical_collide(self, y, field_data) -> bool:
        """
        returns True if block would collide with the bottom of the board or the top of another block
        :param y: y-coord of the block
        :param field_data: current boardstate
        :return: True if collision occurs, otherwise returns nothing
        """
        if not y < ROWS:
            return True

        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True

    def update(self) -> None:
        """Changes current cell sprite position to new one """
        self.rect.topleft =self.pos * CELL_SIZE