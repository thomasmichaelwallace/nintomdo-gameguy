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
        self.action_length = 0
        self.action = 0
        self.init()

    def init(self):
        self.h = 4
        self.w = 2
        self.x = 3
        self.y = 6
        self.action_length = 0
        self.action = 0
        # self.is_ducking = False

    def draw(self, graphics: PicoGraphics):
        graphics.set_pen(screen.PALETTE.white)
        graphics.rectangle(self.x, self.y, self.w, self.h)
        graphics.set_pen(screen.PALETTE.yellow)
        graphics.pixel(self.x + 1, self.y + 1)

    def tick(self):
        if self.action > 0:
            self.action_length -= 1
            print("jump_length:", self.action_length)
        for t, x in level.spikes:
            if x == self.x and t != self.action:
                print("GAME OVER")
                self.init()
                level.init()
                break

    def update(self, dt):
        if self.action > 0:
            if self.action_length < 0:
                if self.action == 1:
                    self.y += 3
                elif self.action == 2:
                    self.w = 2
                    self.h = 4
                    self.y -= 2
                    self.x += 2
                self.action = 0
        elif msa_input.get_jump(dt):
            print("jumping!")
            self.action = 1
            self.action_length = 4
            self.y -= 3
        elif msa_input.get_tilt_as_button(dt) == -1:
            self.action = 2
            self.action_length = 4
            self.y += 2
            self.x -= 2
            self.w = 4
            self.h = 2

class Level:
    def __init__(self):
        self.sky_height = 0
        self.spikes: list[tuple[int, int]] = []
        self.v = 0
        self.t = 0
        self.init()

    def init(self):
        self.sky_height = 10
        self.spikes = [(1, 20)]
        self.v = 0.2
        self.t = 0

    def update(self, dt):
        self.t -= dt
        if self.t < 0:
            self.spikes = [(spike[0], spike[1] - 1) for spike in self.spikes if spike[0] > -2]
            self.t = self.v
            runner.tick()
        if len(self.spikes) == 0:
            self.spikes.append((1, 16))
        else:
            last_spike = self.spikes[-1][1]
            if last_spike < 10:
                if random.random() < 0.2:
                    if random.random() < 0.5:
                        self.spikes.append((1, 16))
                    else:
                        self.spikes.append((2, 16))

    def draw(self, graphics: PicoGraphics):
        graphics.set_pen(screen.PALETTE.blue)
        graphics.rectangle(0, 0, screen.WIDTH, self.sky_height)
        graphics.set_pen(screen.PALETTE.green)
        graphics.rectangle(0, self.sky_height, screen.WIDTH, screen.HEIGHT - self.sky_height)

        for t, x in self.spikes:
            if t == 1:
                graphics.set_pen(screen.PALETTE.red)
                graphics.rectangle(x, self.sky_height - 2, 2, 2)
            elif t == 2:
                graphics.set_pen(screen.PALETTE.orange)
                graphics.rectangle(x, self.sky_height - 4, 2, 2)

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
