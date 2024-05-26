import math
from random import randint
from stellar import StellarUnicorn
from picographics import PicoGraphics
from breakout_msa311 import BreakoutMSA311

# = setup ======================================================================

PALETTE = {}
SCREEN_WIDTH = StellarUnicorn.WIDTH
SCREEN_HEIGHT = StellarUnicorn.HEIGHT

# = entities ===================================================================

class Paddle:
    def __init__(self):
        # layout
        self.width = 5
        # position
        self.y = SCREEN_HEIGHT - 2
        self.x = (SCREEN_WIDTH - self.width) // 2
        # physics
        self.v = 0
        self.v_max = SCREEN_WIDTH * 2.5
        self.a = 2
        self.bounce_c = 0.8
        # input
        self.input_min = 0.075
        self.input_max = 0.6
        self.input_f = self.v_max / (self.input_max - self.input_min)

    def update(self, msa: BreakoutMSA311, dt):
        input_x = -1 * msa.get_x_axis() # x axis is inverted
        clamp_x = max(min(abs(input_x), self.input_max), self.input_min) - self.input_min
        target_v = self.input_f * math.copysign(
            clamp_x, # clamp
            input_x # re-sign
        )
        self.v = self.v + (target_v - self.v) * self.a * dt
        self.x += self.v * dt
        if self.x < 0:
            self.x = 0
            self.v = -self.v * self.bounce_c
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            self.v = -self.v * self.bounce_c

    def draw(self, graphics: PicoGraphics):
        graphics.set_pen(PALETTE["YELLOW"])
        p_x = round(self.x)
        graphics.rectangle(p_x, self.y, self.width, 1)

class Brick:
    def __init__(self, x, y, width, pen):
        self.x = x
        self.y = y
        self.width = width
        self.pen = pen

    def draw(self, graphics: PicoGraphics):
        graphics.set_pen(self.pen)
        graphics.rectangle(self.x, self.y, self.width, 1)

class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.init()

    def init(self):
        self.y = paddle.y - 1
        self.x = paddle.x + paddle.width // 2
        self.vx = randint(-2, 2)
        self.vy = -4

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        # out of bounds
        if self.x < 0:
            self.x = 0
            self.vx = -self.vx
        if self.x > SCREEN_WIDTH - 1:
            self.x = SCREEN_WIDTH - 1
            self.vx = -self.vx
        if self.y < 0:
            self.y = 0
            self.vy = -self.vy

        # game over
        if self.y > SCREEN_HEIGHT + 1:
            self.init()

        # hits paddle
        if check_collision(self, paddle):
            self.vy = -self.vy
            self.y += self.vy * dt * 2

        # hits bricks
        for b in bricks.copy():
            if check_collision(self, b):
                bricks.remove(b)
                self.vy = -self.vy
                self.y += self.vy * dt * 2

    def draw(self, graphics: PicoGraphics):
        graphics.set_pen(PALETTE["WHITE"])
        p_x = round(self.x)
        p_y = round(self.y)
        graphics.pixel(p_x, p_y)

def check_collision(pixel, line):
    p_x = round(pixel.x)
    p_y = round(pixel.y)
    l_y = round(line.y)
    l_x0 = round(line.x)
    l_x1 = round(line.x + line.width)
    if (p_x >= l_x0 and p_x < l_x1) and (p_y == l_y):
        return True
    return False

# = game loop ===================================================================

# init
paddle: Paddle
ball: Ball
bricks: list[Brick]

# loop

def init():
    global paddle, ball, bricks
    paddle = Paddle()
    ball = Ball()
    bricks = [
        # row 1
        Brick(0, 1, 4, PALETTE["GREEN"]),
        Brick(4, 1, 4, PALETTE["DARK_GREEN"]),
        Brick(8, 1, 4, PALETTE["GREEN"]),
        Brick(12, 1, 4, PALETTE["DARK_GREEN"]),
        # row 2
        Brick(2, 2, 3, PALETTE["RED"]),
        Brick(5, 2, 3, PALETTE["ORANGE"]),
        Brick(8, 2, 3, PALETTE["RED"]),
        Brick(11, 2, 3, PALETTE["ORANGE"]),
        # row 3
        Brick(0, 3, 4, PALETTE["BLUE"]),
        Brick(4, 3, 4, PALETTE["DARK_PURPLE"]),
        Brick(8, 3, 4, PALETTE["BLUE"]),
        Brick(12, 3, 4, PALETTE["DARK_PURPLE"]),
        # row 4
        Brick(2, 4, 3, PALETTE["PINK"]),
        Brick(5, 4, 3, PALETTE["BROWN"]),
        Brick(8, 4, 3, PALETTE["PINK"]),
        Brick(11, 4, 3, PALETTE["BROWN"]),
    ]

def update(msa: BreakoutMSA311, dt):
    paddle.update(msa, dt)
    ball.update(dt)

def draw(graphics: PicoGraphics):
    paddle.draw(graphics)
    ball.draw(graphics)
    for brick in bricks:
        brick.draw(graphics)
