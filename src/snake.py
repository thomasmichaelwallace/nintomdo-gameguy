
import random
from picographics import PicoGraphics
import screen
import msa_input

print("DEBUG_1")

# = entities ===================================================================

class Snake:
    def __init__(self):
        self.t = 0
        self.v = 0
        self.dv = 1 - 0.1 # speed increase factor (10% per apple)
        self.dir = 0 # 0: up, 1: right, 2: down, 3: left
        self.body: list[tuple[int, int]] = [] # list of (x, y) tuples
        self.init()

    def init(self):
        self.body = [(8, 8), (9, 8), (10, 8)]
        self.v = 0.5 # initial speed
        self.dir = 1

    def update(self, dt):
        self.t += dt
        if self.t > self.v:
            self.t = 0

            # turn
            input_x = msa_input.get_tilt_float()
            if input_x < 0:
                print("turn left", input_x)
                self.dir -= 1
            elif input_x > 0:
                print("turn right", input_x)
                self.dir += 1
            else:
                print("no turn")
            self.dir = abs(self.dir % 4)

            # move
            x, y = self.body[-1]
            if self.dir == 0:
                y -= 1
            elif self.dir == 1:
                x += 1
            elif self.dir == 2:
                y += 1
            elif self.dir == 3:
                x -= 1
            x = abs(x % screen.WIDTH)
            y = abs(y % screen.HEIGHT)

            # check for collision
            if self.is_grid_taken(x, y):
                print("collision")
                apple.init()
                self.init()

            self.body.append((x, y))

            # check for apple
            if x == apple.x and y == apple.y:
                apple.init()
                self.v *= self.dv
            else:
                self.body.pop(0)


    def is_grid_taken(self, x, y) -> bool:
        for bx, by in self.body:
            if bx == x and by == y:
                return True
        return False

    def draw(self, graphics: PicoGraphics):
        graphics.set_pen(screen.PALETTE.yellow)
        for x, y in self.body:
            graphics.pixel(x, y)

class Apple:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.init()

    def init(self):
        while True:
            self.x = random.randint(0, screen.WIDTH)
            self.y = random.randint(0, screen.HEIGHT)
            if not snake.is_grid_taken(self.x, self.y):
                break

    def draw(self, graphics: PicoGraphics):
        graphics.set_pen(screen.PALETTE.green)
        graphics.pixel(self.x, self.y)

# = game loop ==================================================================

snake: Snake
apple: Apple

def init():
    global snake, apple # pylint: disable=global-statement
    snake = Snake()
    apple = Apple()

def update(dt):
    snake.update(dt)

def draw(graphics: PicoGraphics):
    snake.draw(graphics)
    apple.draw(graphics)
