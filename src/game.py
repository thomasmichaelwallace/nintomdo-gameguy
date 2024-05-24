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
width = StellarUnicorn.WIDTH
height = StellarUnicorn.HEIGHT

print(width, height)

su.set_brightness(0.5)

class Paddle:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width

    def draw(self, graphics):
        graphics.set_pen(graphics.create_pen(255, 255, 0))
        graphics.rectangle(self.x, self.y, self.width, 1)

    def update(self):
        xf = msa.get_x_axis()
        if (xf > 0.1):
            self.x -= 1
        elif (xf < -0.1):
            self.x += 1
        if (self.x < 0):
            self.x = 0
        if (self.x + self.width > width):
            self.x = width - self.width

paddle = Paddle(0, height - 2, 5)

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
