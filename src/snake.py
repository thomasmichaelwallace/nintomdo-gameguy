
from picographics import PicoGraphics
import screen
import msa_input

print("DEBUG_10")

# = entities ===================================================================

class Snake:
    def __init__(self):
        self.t = 0
        self.v = 0
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
            self.body.append((x, y))
            self.body.pop(0)

    def draw(self, graphics: PicoGraphics):
        graphics.set_pen(screen.PALETTE.yellow)
        for x, y in self.body:
            graphics.pixel(x, y)

# = game loop ==================================================================

snake: Snake

def init():
    global snake # pylint: disable=global-statement
    snake = Snake()

def update(dt):
    snake.update(dt)

def draw(graphics: PicoGraphics):
    snake.draw(graphics)
