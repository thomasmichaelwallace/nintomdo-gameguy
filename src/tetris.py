import math
import random
from stellar import StellarUnicorn
from picographics import PicoGraphics
from breakout_msa311 import BreakoutMSA311

# = setup ======================================================================

print("DEBUG_1")

PALETTE = {}
SCREEN_WIDTH = StellarUnicorn.WIDTH
SCREEN_HEIGHT = StellarUnicorn.HEIGHT

# = entities ===================================================================

class Board:
    def __init__(self):
        self.width = 10
        self.height = SCREEN_HEIGHT
        self.x0 = (SCREEN_WIDTH - self.width) // 2
        self.grid = []
        self.lus = 0.5 # rate that lines are cleared
        self.tlus = 0
        self.v = 0
        self.init()

    def init(self):
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.v = 0.25

    def update(self, dt):
        self.tlus += dt
        if self.tlus > self.lus:
            self.tlus = 0
            for j, row in enumerate(self.grid):
                if all(row):
                    print("line cleared!", j)
                    self.grid.pop(j)
                    self.grid.insert(0, [0 for _ in range(self.width)])
                    self.v += 0.1

    def draw(self, graphics: PicoGraphics):
        # walls
        graphics.set_pen(PALETTE["WHITE"])
        graphics.line(self.x0 - 1, 0, self.x0 - 1, self.height)
        graphics.line(self.x0 + self.width, 0, self.x0 + self.width, self.height)
        # blocks
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    graphics.set_pen(cell)
                    graphics.pixel(self.x0 + x, y)

class Tetromino:
    def __init__(self):
        # constants
        self.v_max = SCREEN_WIDTH * 2.5
        self.input_min = 0.075
        self.input_max = 0.6
        self.input_f = self.v_max / (self.input_max - self.input_min)
        # globals
        self.vx = 0.175 # five moves per second
        self.vy = 0.25
        self.tx = 0
        self.ty = 0
        # shape
        self.shape = []
        self.pen = PALETTE["WHITE"]
        self.x = 0
        self.y = 0
        self.init()
        # jump detection
        self.j_thresh = 1.9
        self.j_last = False
        self.j_request = False
        self.j_cool = 1 # time to wait between jumps
        self.j_v = 0
        self.tj = 0
        self.vj = 0.25

    def init(self):
        _, shape_info = random.choice(list(SHAPES.items()))
        self.shape = shape_info["shape"]
        self.pen = PALETTE[shape_info["pen"]]
        # start with shape base at top of board
        self.x = board.width // 2 - len(self.shape[0]) // 2
        self.y = -len(self.shape)
        for _, row in enumerate(self.shape[::-1]):
            if any(row):
                self.y += 1
                break

    def freeze(self):
        for j, row in enumerate(self.shape):
            for i, cell in enumerate(row):
                if cell:
                    board.grid[self.y + j][self.x + i] = self.pen
        if (self.y < 0):
            print("game over")
            board.init()
        self.init()

    def test_collision_x(self):
        for j, row in enumerate(self.shape):
            for i, cell in enumerate(row):
                if cell:
                    if self.x + i < 0:
                        return True
                    elif self.x + i >= board.width:
                        return True
                    elif self.y + j < 0:
                        pass
                    elif self.y + j >= board.height:
                        pass
                    elif board.grid[self.y + j][self.x + i]:
                        return True
        return False

    def test_collision_y(self):
        for j, row in enumerate(self.shape):
            for i, cell in enumerate(row):
                if cell:
                    if self.y + j >= board.height:
                        return True
                    if self.y + j >= 0 and board.grid[self.y + j][self.x + i]:
                        return True
        return False


    def update(self, msa: BreakoutMSA311, dt):
        # jump detection
        spin = False
        y = msa.get_y_axis()
        if self.tj > 0 and y > self.j_thresh:
            if not self.j_last:
                self.j_request = True
                self.j_v = y
        else:
            self.j_last = False
        self.tj += dt
        if self.tj > self.vj:
            self.tj = 0
            if self.j_request:
                self.j_request = False
                self.tj = self.vj - self.j_cool
                print("spin!", self.j_v)
                spin = True

        if spin:
            self.shape = list(zip(*self.shape[::-1]))
            if self.test_collision_x():
                self.shape = list(zip(*self.shape[::-1]))
            if self.test_collision_y():
                self.shape = list(zip(*self.shape[::-1]))

        # x-movement
        self.tx += dt
        input_x = 0
        if self.tx > self.vx:
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

        # x collision
        if input_x != 0:
            if self.test_collision_x():
                if input_x < 0:
                    self.x += 1
                elif input_x > 0:
                    self.x -= 1

        # y-movement and collision
        self.ty += dt
        if self.ty > self.vy:
            self.ty = 0
            self.y += 1
            if self.test_collision_y():
                self.y -= 1
                self.freeze()

    def draw(self, graphics: PicoGraphics):
        for j, row in enumerate(self.shape):
            for i, cell in enumerate(row):
                if cell:
                    dx = self.x + i + board.x0
                    dy = self.y + j
                    graphics.set_pen(self.pen)
                    graphics.pixel(dx, dy)

# = resources ==================================================================

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
tetromino: Tetromino

# loop

def init():
    global board, tetromino
    board = Board()
    tetromino = Tetromino()

def update(msa: BreakoutMSA311, dt):
    board.update(dt)
    tetromino.update(msa, dt)

def draw(graphics: PicoGraphics):
    board.draw(graphics)
    tetromino.draw(graphics)
