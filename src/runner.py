import random
from picographics import PicoGraphics
import msa_input
import screen

print("DEBUG_1")

# = entities ===================================================================

class Runner:
    def __init__(self):
        # constants
        self.action_duration = 0.5
        # inits
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.action_timer = 0
        self.is_jumping = False
        self.is_ducking = False
        self.init()

    def init(self):
        self.h = 4
        self.w = 2
        self.x = 3
        self.y = 16 - 4 - self.h
        self.action_timer = 0
        self.is_jumping = False
        self.is_ducking = False

    def draw(self, graphics: PicoGraphics):
        graphics.set_pen(screen.PALETTE.white)
        graphics.rectangle(self.x, self.y, self.w, self.h)

    def update(self, dt):
        if self.is_jumping:
            self.action_timer -= dt
            if self.action_timer <= 0:
                self.is_jumping = False
                self.y += self.h
        elif self.is_ducking:
            self.action_timer -= dt
            if self.action_timer <= 0:
                self.is_ducking = False
                oh = self.h
                ow = self.w
                self.h = ow
                self.w = oh
                self.y -= (self.h - self.w)
        elif msa_input.get_jump(dt):
            print("jumping!")
            self.y -= self.h
            self.is_jumping = True
            self.action_timer = self.action_duration
        elif msa_input.get_tilt_as_button(dt) == -1:
            print("sliding")
            self.y += (self.h - self.w)
            oh = self.h
            ow = self.w
            self.h = ow
            self.w = oh
            self.is_ducking = True
            self.action_timer = self.action_duration

class Level:
    def __init__(self):
        self.init()

    def init(self):
        self.obstacles = []
        self.obstacle_timer = 0
        self.obstacle_interval = 1

    def update(self, dt):
        self.obstacle_timer -= dt
        if self.obstacle_timer <= 0:
            self.obstacle_timer = self.obstacle_interval
            self.obstacles.append(Obstacle())

    def draw(self, graphics: PicoGraphics):
        for obstacle in self.obstacles:
            obstacle.draw(graphics)

class Obstacle:
    def __init__(self):
        self.init()

    def init(self):
        self.x = 128
        self.y = 16 - 4
        self.w = 2
        self.h = 4
        self.speed = 10

    def draw(self, graphics: PicoGraphics):
        graphics.set_pen(screen.PALETTE.red)
        graphics.rectangle(self.x, self.y, self.w, self.h)

    def update(self, dt):
        self.x -= self.speed * dt

        if self.x < 0:
            self.x = 128
            self.speed = random.randint(10, 20)


# = game loop ==================================================================

runner: Runner

def init():
    global runner # pylint: disable=global-statement
    runner = Runner()

def update(dt):
    runner.update(dt)

def draw(graphics: PicoGraphics):
    runner.draw(graphics)
