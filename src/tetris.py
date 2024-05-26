import math
import random
from stellar import StellarUnicorn
from picographics import PicoGraphics
from breakout_msa311 import BreakoutMSA311

# = setup ======================================================================

PALETTE = {}
SCREEN_WIDTH = StellarUnicorn.WIDTH
SCREEN_HEIGHT = StellarUnicorn.HEIGHT

class Board:
    def __init__(self):
        self.width = 10
        self.height = SCREEN_HEIGHT
        self.x0 = (SCREEN_WIDTH - self.width) // 2
        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]

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
        self.init()

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
        self.t = 0
        self.v = 0.25

    def freeze(self):
        for j, row in enumerate(self.shape):
            for i, cell in enumerate(row):
                if cell:
                    board.grid[self.y + j][self.x + i] = self.pen
        self.init()


    def update(self, msa: BreakoutMSA311, dt):
        self.t += dt
        if self.t > self.v:
            self.t = 0
            self.y += 1
        # y collision
        for j, row in enumerate(self.shape):
            for i, cell in enumerate(row):
                if cell:
                    if self.y + j >= board.height:
                        self.y -= 1
                        self.freeze()
                        return
                    if self.y + j >= 0 and board.grid[self.y + j][self.x + i]:
                        self.y -= 1
                        self.freeze()
                        return

    def draw(self, graphics: PicoGraphics):
        for j, row in enumerate(self.shape):
            for i, cell in enumerate(row):
                if cell:
                    dx = self.x + i + board.x0
                    dy = self.y + j
                    graphics.set_pen(self.pen)
                    graphics.pixel(dx, dy)

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

board: Board
tetromino: Tetromino

def init():
    global board, tetromino
    board = Board()
    tetromino = Tetromino()

def update(msa: BreakoutMSA311, dt):
    tetromino.update(msa, dt)

def draw(graphics: PicoGraphics):
    board.draw(graphics)
    tetromino.draw(graphics)
