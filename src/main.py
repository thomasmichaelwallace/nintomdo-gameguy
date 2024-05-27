import time
from stellar import StellarUnicorn
from picographics import PicoGraphics, DISPLAY_STELLAR_UNICORN as DISPLAY
import msa_input
import screen

# global options

DEBUG_MODE=0
print("DEBUG_MODE:", DEBUG_MODE)

# global hardware references
stellar = StellarUnicorn()
graphics = PicoGraphics(DISPLAY)

# global setup
screen.screen_init(graphics)

BRIGHTNESS = 1
if DEBUG_MODE > 0:
    BRIGHTNESS = 0.3 # do not blind myself while working with the board directly
stellar.set_brightness(BRIGHTNESS)

# timer
FPS = 30
DT_MS = round(1000/FPS)

# title screen

GAME = None

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
    # note that import is relative to main.py in root
    if DEBUG_MODE == 1 or stellar.is_pressed(StellarUnicorn.SWITCH_A):
        import breakout as GAME
    if DEBUG_MODE == 2 or stellar.is_pressed(StellarUnicorn.SWITCH_B):
        import tetris as GAME
    if DEBUG_MODE == -1:
        GAME = screen

    if GAME:
        break

    time.sleep_ms(DT_MS)

# game loop

GAME.init()

while True:
    # board
    if stellar.is_pressed(StellarUnicorn.SWITCH_BRIGHTNESS_UP):
        BRIGHTNESS = min(BRIGHTNESS + 0.01, 1.0)
        stellar.set_brightness(BRIGHTNESS)
    if stellar.is_pressed(StellarUnicorn.SWITCH_BRIGHTNESS_DOWN):
        BRIGHTNESS = max(BRIGHTNESS - 0.01, 0.0)
        stellar.set_brightness(BRIGHTNESS)

    # game
    msa_input.update(DT_MS / 1000)
    GAME.update(DT_MS / 1000)

    graphics.set_pen(screen.PALETTE.black)
    graphics.clear()
    GAME.draw(graphics)

    stellar.update(graphics)

    time.sleep_ms(DT_MS)
