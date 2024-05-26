import time
from stellar import StellarUnicorn
from picographics import PicoGraphics, DISPLAY_STELLAR_UNICORN as DISPLAY
from pimoroni_i2c import PimoroniI2C
from breakout_msa311 import BreakoutMSA311

# global hardware references
stellar = StellarUnicorn()
graphics = PicoGraphics(DISPLAY)    

# setup msa311 (accelerometer) breakout board
PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
msa = BreakoutMSA311(i2c)

FPS = 30
DT_MS = round(1000/FPS)

def hex_to_pen(gfx, hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    pen = gfx.create_pen(r, g, b)
    return pen
# (https://lospec.com/palette-list/pico-8):
PALETTE = {
    "BLACK": hex_to_pen(graphics, "#000000"),
    "DARK_BLUE": hex_to_pen(graphics, "#1d2b53"),
    "DARK_PURPLE": hex_to_pen(graphics, "#7e2553"),
    "DARK_GREEN": hex_to_pen(graphics, "#008751"),
    "BROWN": hex_to_pen(graphics, "#ab5236"),
    "DARK_GRAY": hex_to_pen(graphics, "#5f574f"),
    "LIGHT_GRAY": hex_to_pen(graphics, "#c2c3c7"),
    "WHITE": hex_to_pen(graphics, "#fff1e8"),
    "RED": hex_to_pen(graphics, "#ff004d"),
    "ORANGE": hex_to_pen(graphics, "#ffa300"),
    "YELLOW": hex_to_pen(graphics, "#ffec27"),
    "GREEN": hex_to_pen(graphics, "#00e436"),
    "BLUE": hex_to_pen(graphics, "#29adff"),
    "INDIGO": hex_to_pen(graphics, "#83769c"),
    "PINK": hex_to_pen(graphics, "#ff77a8"),
    "PEACH": hex_to_pen(graphics, "#ffccaa"),
}

brightness = 0.5

stellar.set_brightness(brightness)

# title screen

game = None

graphics.set_pen(graphics.create_pen(255, 0, 0))
graphics.pixel(0, 3)
graphics.set_pen(graphics.create_pen(0, 255, 0))
graphics.pixel(0, 5)
graphics.set_pen(graphics.create_pen(0, 0, 255))
graphics.pixel(0, 7)
graphics.set_pen(graphics.create_pen(255, 0, 255))
graphics.pixel(0, 9)
stellar.update(graphics)

while True:
    if stellar.is_pressed(StellarUnicorn.SWITCH_A):
        import breakout as game

    if game:
        game.PALETTE = PALETTE
        game.init()
        break

    time.sleep_ms(DT_MS)

# game loop

while True:
    # board
    if stellar.is_pressed(StellarUnicorn.SWITCH_BRIGHTNESS_UP):
        brightness = min(brightness + 0.01, 1.0)
        stellar.set_brightness(brightness)
    if stellar.is_pressed(StellarUnicorn.SWITCH_BRIGHTNESS_DOWN):
        brightness = max(brightness - 0.01, 0.0)
        stellar.set_brightness(brightness)

    # game
    game.update(msa, DT_MS / 1000)

    graphics.set_pen(PALETTE["BLACK"])
    graphics.clear()
    game.draw(graphics)

    stellar.update(graphics)

    time.sleep_ms(DT_MS)