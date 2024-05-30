import random
from picographics import PicoGraphics
import msa_input
import screen

print("DEBUG_2")

# = entities ===================================================================

class Runner:
    def __init__(self):
        # inits
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.jump_length = 0
        self.is_jumping = False
        # self.is_ducking = False
        self.init()

    def init(self):
        self.h = 4
        self.w = 2
        self.x = 3
        self.y = 6
        self.jump_length = 0
        self.is_jumping = False
        # self.is_ducking = False

    def draw(self, graphics: PicoGraphics):
        graphics.set_pen(screen.PALETTE.white)
        graphics.rectangle(self.x, self.y, self.w, self.h)
        graphics.set_pen(screen.PALETTE.yellow)
        graphics.pixel(self.x + 1, self.y + 1)

    def tick(self):
        if self.is_jumping:
            self.jump_length -= 1
            print("jump_length:", self.jump_length)
        else:
            for spike in level.spikes:
                if spike == self.x:
                    print("GAME OVER")
                    self.init()
                    level.init()
                    break


    def update(self, dt):
        if self.is_jumping:
            if self.jump_length < 0:
                self.is_jumping = False
                self.y += 3
        elif msa_input.get_jump(dt):
            print("jumping!")
            self.y -= 3
            self.is_jumping = True
            self.jump_length = 4

class Level:
    def __init__(self):
        self.sky_height = 0
        self.spikes = []
        self.v = 0
        self.t = 0
        self.init()

    def init(self):
        self.sky_height = 10
        self.spikes = [20]
        self.v = 0.2
        self.t = 0

    def update(self, dt):
        self.t -= dt
        if self.t < 0:
            self.spikes = [spike - 1 for spike in self.spikes if spike > -2]
            self.t = self.v
            runner.tick()
        if len(self.spikes) == 0:
            self.spikes.append(16)
        else:
            last_spike = self.spikes[-1]
            if last_spike < 10:
                if random.random() < 0.2:
                    self.spikes.append(16)



    def draw(self, graphics: PicoGraphics):
        graphics.set_pen(screen.PALETTE.blue)
        graphics.rectangle(0, 0, screen.WIDTH, self.sky_height)
        graphics.set_pen(screen.PALETTE.green)
        graphics.rectangle(0, self.sky_height, screen.WIDTH, screen.HEIGHT - self.sky_height)

        for spike in self.spikes:
            graphics.set_pen(screen.PALETTE.red)
            graphics.rectangle(spike, self.sky_height - 2, 2, 2)

# = game loop ==================================================================

runner: Runner
level: Level

def init():
    global runner, level # pylint: disable=global-statement
    level = Level()
    runner = Runner()

def update(dt):
    level.update(dt)
    runner.update(dt)

def draw(graphics: PicoGraphics):
    level.draw(graphics)
    runner.draw(graphics)
