from random import randint
from picographics import PicoGraphics
import msa_input
import screen

print("DEBUG_6")

# = entities ===================================================================

class Paddle: # pylint: disable=too-many-instance-attributes
    def __init__(self):
        # layout
        self.width = 5
        # position
        self.y = screen.HEIGHT - 2
        self.x = 0
        # physics
        self.v = 0
        self.v_max = screen.WIDTH * 2.5
        self.a = 2
        self.bounce_c = 0.8
        # input
        self.input_f = self.v_max

    def init(self):
        self.x = (screen.WIDTH - self.width) // 2
        self.v = 0

    def update(self, dt):
        target_v = self.input_f * msa_input.get_tilt_float()
        self.v = self.v + (target_v - self.v) * self.a * dt
        self.x += self.v * dt
        if self.x < 0:
            self.x = 0
            self.v = -self.v * self.bounce_c
        if self.x > screen.WIDTH - self.width:
            self.x = screen.WIDTH - self.width
            self.v = -self.v * self.bounce_c

    def draw(self, graphics: PicoGraphics):
        graphics.set_pen(screen.PALETTE.yellow)
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
        if self.x > screen.WIDTH - 1:
            self.x = screen.WIDTH - 1
            self.vx, self.vy =  reflect_vector([self.vx, self.vy], [-1, 0])
        if self.y < 0:
            self.y = 0
            self.vx, self.vy = reflect_vector([self.vx, self.vy], [0, -1])

        # game over
        if self.y > screen.HEIGHT + 1:
            level.ball_lost()

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
        graphics.set_pen(screen.PALETTE.white)
        p_x = round(self.x)
        p_y = round(self.y)
        graphics.pixel(p_x, p_y)

class Level:
    def __init__(self):
        self.lives = 0
        self.init()

    def init(self):
        self.lives = 3
        bricks.clear()
        for b in [
            # row 1
            Brick(0, 1, 4, screen.PALETTE.green),
            Brick(4, 1, 4, screen.PALETTE.red),
            Brick(8, 1, 4, screen.PALETTE.green),
            Brick(12, 1, 4, screen.PALETTE.red),
            # row 2
            Brick(2, 2, 3, screen.PALETTE.orange),
            Brick(5, 2, 3, screen.PALETTE.azure),
            Brick(8, 2, 3, screen.PALETTE.orange),
            Brick(11, 2, 3, screen.PALETTE.azure),
            # row 3
            Brick(0, 3, 4, screen.PALETTE.indigo),
            Brick(4, 3, 4, screen.PALETTE.yellow),
            Brick(8, 3, 4, screen.PALETTE.indigo),
            Brick(12, 3, 4, screen.PALETTE.yellow),
            # row 4
            Brick(2, 4, 3, screen.PALETTE.spring_green),
            Brick(5, 4, 3, screen.PALETTE.pink),
            Brick(8, 4, 3, screen.PALETTE.spring_green),
            Brick(11, 4, 3, screen.PALETTE.pink),
        ]:
            bricks.append(b)
        paddle.init()
        ball.init()


    def draw(self, graphics: PicoGraphics):
        graphics.set_pen(screen.PALETTE.white)
        for i in range(self.lives):
            graphics.pixel(i * 2, 0)

    def ball_lost(self):
        self.lives -= 1
        if self.lives < 0:
            self.init()
        else:
            ball.init()

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
bricks: list[Brick] = []
level: Level

# loop

def init():
    global paddle, ball, level # pylint: disable=global-statement
    paddle = Paddle()
    ball = Ball()
    level = Level()

def update(dt):
    paddle.update(dt)
    ball.update(dt)

def draw(graphics: PicoGraphics):
    level.draw(graphics)
    paddle.draw(graphics)
    ball.draw(graphics)
    for brick in bricks:
        brick.draw(graphics)
