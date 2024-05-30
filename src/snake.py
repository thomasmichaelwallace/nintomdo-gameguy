
import random
from picographics import PicoGraphics
import screen
import msa_input

print("DEBUG_4")

# = entities ===================================================================

class Snake:
    def __init__(self):
        self.t = 0
        self.v = 0
        self.last_button = 0
        self.dv = 1 - 0.1 # speed increase factor (10% per apple)

        self.dir = 0 # 0: up, 1: right, 2: down, 3: left
        self.body: list[tuple[int, int]] = [] # list of (x, y) tuples
        self.init()

    def init(self):
        self.body = [(8, 8), (9, 8), (10, 8)]
        self.v = 0.5 # initial speed
        self.dir = 1

    def update(self, dt):
        input_x = msa_input.get_tilt_as_button(dt)
        if input_x != 0:
            self.last_button = input_x

        self.t += dt
        if self.t > self.v:
            self.t = 0

            # turn
            if self.last_button < 0:
                self.dir += 1
            elif self.last_button > 0:
                self.dir -= 1
            self.dir = abs(self.dir % 4)
            self.last_button = 0

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
                return
            if course.is_wall(x, y):
                print("wall collision")
                apple.init()
                self.init()
                return

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
            self.x = random.randint(0, screen.WIDTH - 1)
            self.y = random.randint(0, screen.HEIGHT - 1)
            if not snake.is_grid_taken(self.x, self.y) and not course.is_wall(self.x, self.y):
                print("apple at", self.x, self.y)
                break

    def draw(self, graphics: PicoGraphics):
        graphics.set_pen(screen.PALETTE.green)
        graphics.pixel(self.x, self.y)

class Course:
    def __init__(self):
        walls = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        self.px = []
        for y, row in enumerate(walls):
            for x, cell in enumerate(row):
                if cell == 1:
                    self.px.append((x, y))


    def draw(self, graphics: PicoGraphics):
        for x, y in self.px:
            graphics.set_pen(screen.PALETTE.red)
            graphics.pixel(x, y)

    def is_wall(self, x, y) -> bool:
        return (x, y) in self.px

# = game loop ==================================================================

snake: Snake
apple: Apple
course: Course

def init():
    global snake, apple, course # pylint: disable=global-statement
    course = Course()
    snake = Snake()
    apple = Apple()

def update(dt):
    snake.update(dt)

def draw(graphics: PicoGraphics):
    course.draw(graphics)
    snake.draw(graphics)
    apple.draw(graphics)
