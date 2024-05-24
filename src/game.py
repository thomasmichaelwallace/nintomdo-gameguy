import time
from stellar import StellarUnicorn
from picographics import PicoGraphics, DISPLAY_STELLAR_UNICORN as DISPLAY
from pimoroni_i2c import PimoroniI2C
from breakout_msa311 import BreakoutMSA311

# setup msa311 (accelerometer) breakout board
PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
msa = BreakoutMSA311(i2c)

# setup stellar unicorn (led matrix)
su = StellarUnicorn()
graphics = PicoGraphics(DISPLAY)
WIDTH = StellarUnicorn.WIDTH
HEIGHT = StellarUnicorn.HEIGHT

print(WIDTH, HEIGHT)

su.set_brightness(0.5)

class Paddle:
    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.width = w

    def draw(self, g):
        graphics.set_pen(g.create_pen(255, 255, 0))
        graphics.rectangle(self.x, self.y, self.width, 1)

    def update(self):
        xf = msa.get_x_axis()
        if xf > 0.1:
            self.x -= 1
        elif xf < -0.1:
            self.x += 1
        self.x = max(0, self.x)
        self.x = min(WIDTH - self.width, self.x)

paddle = Paddle(0, HEIGHT - 2, 5)

# game loop
while True:
    # update
    paddle.update()

    # clear screen
    graphics.set_pen(graphics.create_pen(0, 0, 0))
    graphics.clear()

    # draw
    paddle.draw(graphics)

    su.update(graphics)

    time.sleep(1/25)
