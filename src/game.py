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

# game loop
while True:
    xf = msa.get_x_axis()

    x = int((-xf + 1) * width / 2)
    y = height // 2 # center y
    print(x, y)
    
    graphics.set_pen(graphics.create_pen(0, 0, 0))
    graphics.clear()
    graphics.set_pen(graphics.create_pen(255, 255, 255))
    graphics.pixel(x, y)

    su.update(graphics)

    time.sleep(0.1)
