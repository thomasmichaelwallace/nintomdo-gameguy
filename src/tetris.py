import math
import random
from stellar import StellarUnicorn
from picographics import PicoGraphics
from breakout_msa311 import BreakoutMSA311

# = setup ======================================================================

print("DEBUG_6")

PALETTE = {}
SCREEN_WIDTH = StellarUnicorn.WIDTH
SCREEN_HEIGHT = StellarUnicorn.HEIGHT

# = entities ===================================================================

class Board: # pylint: disable=too-many-instance-attributes
    def __init__(self):
        # constants
        self.width = 10
        self.height = SCREEN_HEIGHT
        self.left = (SCREEN_WIDTH - self.width) // 2
        self.initial_fall_speed = 0.6
        self.next_level_speed_factor = 1- 0.2 # increase speed by 20%
        self.t = 0
        self.check_line_interval = 0.5 # rate that lines are cleared
        # init vars
        self.grid = []
        self.move_y_interval = 0
        self.init()

    def init(self):
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.move_y_interval = self.initial_fall_speed

    def is_grid_taken(self, x, y) -> bool:
        if x < 0 or x >= self.width:
            return True
        if y >= self.height:
            return True
        if y < 0:
            return False
        return self.grid[y][x] != 0

    def set_grid_position(self, x, y, pen):
        if (0 <= y < self.height) and (0 <= x < self.width):
            self.grid[y][x] = pen

    def update(self, dt):
        self.t += dt
        if self.t > self.check_line_interval:
            self.t = 0
            for j, row in enumerate(self.grid):
                if all(row):
                    print("line cleared!", j)
                    self.grid.pop(j)
                    self.grid.insert(0, [0 for _ in range(self.width)])
                    self.move_y_interval *= self.next_level_speed_factor

    def draw(self, graphics: PicoGraphics):
        # walls
        graphics.set_pen(PALETTE["WHITE"])
        graphics.line(self.left - 1, 0, self.left - 1, self.height)
        graphics.line(self.left + self.width, 0, self.left + self.width, self.height)
        # blocks
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    graphics.set_pen(cell)
                    graphics.pixel(self.left + x, y)

class Block: # pylint: disable=too-many-instance-attributes
    def __init__(self):
        # constants
        self.jump_g_threshold = 1.9
        self.jump_requested = False
        self.jump_cooldown_interval = 1 # time to wait between jumps
        self.tj = 0
        self.jump_check_interval = 0.25
        self.jump_velocity = 0
        self.input_min = 0.075
        self.input_max = 0.6
        self.tx = 0
        self.move_x_check_interval = 0.25 # five moves per second
        self.ty = 0
        # init
        self.x = 0
        self.y = 0
        self.rotation = 0
        self.shape = []
        self.shape_name = "I"
        self.pen = PALETTE["WHITE"]
        self.init()

    def init(self):
        name, shape_info = random.choice(list(SHAPES.items()))
        self.shape_name = name
        self.shape = shape_info["shape"]
        self.pen = PALETTE[shape_info["pen"]]
        # start with shape in origin rotation with base line just above board
        self.rotation = 0
        self.x = board.width // 2 - len(self.shape[0]) // 2
        self.y = -len(self.shape)
        for _, row in enumerate(self.shape[::-1]):
            if any(row):
                self.y += 1
                break

    def place_block(self):
        for j, row in enumerate(self.shape):
            for i, cell in enumerate(row):
                if cell:
                    board.set_grid_position(self.x + i, self.y + j, self.pen)
        if self.y < 0:
            print("game over")
            board.init()
        self.init()

    def test_collision(self):
        for j, row in enumerate(self.shape):
            for i, cell in enumerate(row):
                if cell:
                    cx = self.x + i
                    cy = self.y + j
                    if board.is_grid_taken(cx, cy):
                        return True
        return False

    def try_rotate_with_kick(self):
        rule_set = KICK_RULES["I"] if self.shape_name == "I" else KICK_RULES["NOT_I"]
        rules = rule_set[self.rotation % 4]
        self.shape = [list(row)[::-1] for row in zip(*self.shape)]
        xo = self.x
        yo = self.y
        for rule in rules:
            dx, dy = rule
            self.x = xo + dx # dx is right-wards
            self.y = yo - dy # dy is up-wards
            if not self.test_collision():
                self.rotation += 1
                return True
        self.shape = list(reversed(list(zip(*self.shape))))
        self.x = xo
        self.y = yo
        return False

    def jump_detected(self, msa, dt) -> bool:
        y = msa.get_y_axis()
        self.tj += dt
        if self.tj > 0 and y > self.jump_g_threshold:
            self.jump_requested = True
            self.jump_velocity = max(self.jump_requested, y)
        if self.tj > self.jump_check_interval:
            self.tj = 0
            if self.jump_requested:
                self.jump_requested = False
                self.jump_velocity = 0
                self.tj = self.jump_check_interval - self.jump_cooldown_interval
                print("jump!", self.jump_velocity)
                return True
        return False

    def update(self, msa: BreakoutMSA311, dt):
        # rotate
        if self.jump_detected(msa, dt):
            if self.try_rotate_with_kick():
                pass
            else:
                print("rotate blocked")

        # x movement
        self.tx += dt
        input_x = 0
        if self.tx > self.move_x_check_interval:
            self.tx = 0
            input_x = -1 * msa.get_x_axis() # x axis is inverted
            clamp_x = max(min(abs(input_x), self.input_max), self.input_min) - self.input_min
            input_x = math.copysign(
                clamp_x, # clamp
                input_x # re-sign
            )
            if input_x < 0:
                self.x -= 1
            elif input_x > 0:
                self.x += 1
        if input_x != 0:
            if self.test_collision():
                if input_x < 0:
                    self.x += 1
                elif input_x > 0:
                    self.x -= 1

        # fall
        self.ty += dt
        if self.ty > board.move_y_interval:
            self.ty = 0
            self.y += 1
            if self.test_collision():
                self.y -= 1
                self.place_block()

    def draw(self, graphics: PicoGraphics):
        for j, row in enumerate(self.shape):
            for i, cell in enumerate(row):
                if cell:
                    dx = self.x + i + board.left
                    dy = self.y + j
                    graphics.set_pen(self.pen)
                    graphics.pixel(dx, dy)

# = resources ==================================================================

KICK_RULES = {
    "NOT_I": [
        [[0,0], [-1,0], [-1, 1], [0,-2], [-1,-2]], # O -> R
        [[0,0], [ 1,0], [ 1,-1], [0, 2], [ 1, 2]], # R -> 2
        [[0,0], [ 1,0], [ 1, 1], [0,-2], [ 1,-2]], # 2 -> L
        [[0,0], [-1,0], [-1,-1], [0, 2], [-1, 2]], # L -> O
    ],
    "I": [
        [[0,0], [-2,0], [ 1,0], [-2,-1], [ 1, 2]], # O -> R
        [[0,0], [-1,0], [ 2,0], [-1, 2], [ 2,-1]], # R -> 2
        [[0,0], [ 2,0], [-1,0], [ 2, 1], [-1,-2]], # 2 -> L
        [[0,0], [ 1,0], [-2,0], [ 1,-2], [-2, 1]], # L -> O
    ]
}

SHAPES = {
    "I": {
        "shape": [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        "pen": "CYAN"
    },
    "J": {
        "shape": [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0],
        ],
        "pen": "BLUE"
    },
    "L": {
        "shape": [
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0],
        ],
        "pen": "ORANGE"
    },
    "O": {
        "shape": [
            [1, 1],
            [1, 1],
        ],
        "pen": "YELLOW"
    },
    "S": {
        "shape": [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0],
        ],
        "pen": "GREEN"
    },
    "T": {
        "shape": [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0],
        ],
        "pen": "PURPLE"
    },
    "Z": {
        "shape": [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0],
        ],
        "pen": "RED"
    }
}

# = game loop ===================================================================

# init
board: Board
tetromino: Block

# loop

def init():
    global board, tetromino # pylint: disable=global-statement
    board = Board()
    tetromino = Block()

def update(msa: BreakoutMSA311, dt):
    board.update(dt)
    tetromino.update(msa, dt)

def draw(graphics: PicoGraphics):
    board.draw(graphics)
    tetromino.draw(graphics)
