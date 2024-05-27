from random import randint
from stellar import StellarUnicorn
from picographics import PicoGraphics
import msa_input

# = setup ======================================================================

print("DEBUG_8")

PALETTE = {}
SCREEN_WIDTH = StellarUnicorn.WIDTH
SCREEN_HEIGHT = StellarUnicorn.HEIGHT

# = entities ===================================================================

class Paddle: # pylint: disable=too-many-instance-attributes
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
        self.input_f = self.v_max

    def update(self, dt):
        target_v = self.input_f * msa_input.get_tilt_float()
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

class Brick: # pylint: disable=too-few-public-methods
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
            self.vx, self.vy = reflect_vector([self.vx, self.vy], [1, 0])
        if self.x > SCREEN_WIDTH - 1:
            self.x = SCREEN_WIDTH - 1
            self.vx, self.vy =  reflect_vector([self.vx, self.vy], [-1, 0])
        if self.y < 0:
            self.y = 0
            self.vx, self.vy = reflect_vector([self.vx, self.vy], [0, -1])

        # game over
        if self.y > SCREEN_HEIGHT + 1:
            self.init()

        # hits paddle
        if check_collision(self, paddle):
            self.y = paddle.y - 1
            # get position on paddle
            offset = self.x - paddle.x
            if offset < 1:
                self.vx, self.vy = reflect_vector([self.vx, self.vy], [0.196, 0.981])
                print("very left")
            elif offset > 4:
                self.vx, self.vy = reflect_vector([self.vx, self.vy], [-0.196, 0.981])
                print("very right")
            else:
                self.vx, self.vy = reflect_vector([self.vx, self.vy], [0, 1])
                print("center")

        # hits bricks
        for b in bricks.copy():
            if check_collision(self, b):
                bricks.remove(b)
                self.vy = -self.vy

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
    if l_x0 <= p_x < l_x1 and p_y == l_y:
        return True
    return False

def dot_product(vm, nm):
    return sum(v*n for v, n in zip(vm, nm))

def magnitude(nm):
    return sum(n**2 for n in nm)**0.5

def reflect_vector(vm, nm):
    nm = [n / magnitude(nm) for n in nm]
    rm = [v - 2 * dot_product(vm, nm) * n for v, n in zip(vm, nm)]
    return rm

# = game loop ===================================================================

# init
paddle: Paddle
ball: Ball
bricks: list[Brick]

# loop

def init():
    global paddle, ball, bricks # pylint: disable=global-statement
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

def update(dt):
    paddle.update(dt)
    ball.update(dt)

def draw(graphics: PicoGraphics):
    paddle.draw(graphics)
    ball.draw(graphics)
    for brick in bricks:
        brick.draw(graphics)
