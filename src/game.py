import time
from stellar import StellarUnicorn
from picographics import PicoGraphics, DISPLAY_STELLAR_UNICORN as DISPLAY
from pimoroni_i2c import PimoroniI2C
from breakout_msa311 import BreakoutMSA311

# = setup ======================================================================

# setup msa311 (accelerometer) breakout board
PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
msa = BreakoutMSA311(i2c)

# setup stellar unicorn (led matrix)
su = StellarUnicorn()
graphics = PicoGraphics(DISPLAY)

def hex_to_pen(gfx, hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    pen = gfx.create_pen(r, g, b)
    return pen
# (https://lospec.com/palette-list/pico-8):
PEN_BLACK=hex_to_pen(graphics, "#000000")
PEN_DARK_BLUE=hex_to_pen(graphics, "#1d2b53")
PEN_DARK_PURPLE=hex_to_pen(graphics, "#7e2553")
PEN_DARK_GREEN=hex_to_pen(graphics, "#008751")
PEN_BROWN=hex_to_pen(graphics, "#ab5236")
PEN_DARK_GRAY=hex_to_pen(graphics, "#5f574f")
PEN_LIGHT_GRAY=hex_to_pen(graphics, "#c2c3c7")
PEN_WHITE=hex_to_pen(graphics, "#fff1e8")
PEN_RED=hex_to_pen(graphics, "#ff004d")
PEN_ORANGE=hex_to_pen(graphics, "#ffa300")
PEN_YELLOW=hex_to_pen(graphics, "#ffec27")
PEN_GREEN=hex_to_pen(graphics, "#00e436")
PEN_BLUE=hex_to_pen(graphics, "#29adff")
PEN_INDIGO=hex_to_pen(graphics, "#83769c")
PEN_PINK=hex_to_pen(graphics, "#ff77a8")
PEN_PEACH=hex_to_pen(graphics, "#ffccaa")

SCREEN_WIDTH = StellarUnicorn.WIDTH
SCREEN_HEIGHT = StellarUnicorn.HEIGHT

su.set_brightness(0.4)

# = options ====================================================================

FPS = 30
DT = 1/FPS

# = entities ===================================================================

class Paddle:
    def __init__(self):
        self.width = 5
        self.y = SCREEN_HEIGHT - 2
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.v_x = 0
        self.bounce_c = 0.2
        self.g_factor = 9.81 * 3;

    def draw(self):
        graphics.set_pen(PEN_YELLOW)
        p_x = int(self.x) 
        graphics.rectangle(p_x, self.y, self.width, 1)

    def update(self):
        input_x = -1 * msa.get_x_axis() # x axis is inverted
        acc_x = self.g_factor * input_x # input is normalized to gravity
        self.v_x = self.v_x + acc_x * DT
        self.x += self.v_x * DT
        if self.x < 0:
            self.x = 0
            self.v_x = -self.v_x * self.bounce_c
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            self.v_x = -self.v_x * self.bounce_c

# = game loop ===================================================================

# init
paddle = Paddle()

print("Game started")

# loop
while True:
    # _update
    paddle.update()

    # _draw
    graphics.set_pen(PEN_BLACK)
    graphics.clear()
    paddle.draw()
    su.update(graphics)

    time.sleep(DT)
