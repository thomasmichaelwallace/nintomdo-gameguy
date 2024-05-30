import time
from stellar import StellarUnicorn
from picographics import PicoGraphics, DISPLAY_STELLAR_UNICORN as DISPLAY
import msa_input
import screen

# global options

DEBUG_MODE=0
print("DEBUG_MODE:", DEBUG_MODE)
print("DEBUG_123")

# start screen
stellar = StellarUnicorn()
graphics = PicoGraphics(DISPLAY)
screen.screen_init(graphics)
BRIGHTNESS = 1
if DEBUG_MODE > 0:
    BRIGHTNESS = 0.3 # do not blind myself while working with the board directly
stellar.set_brightness(BRIGHTNESS)

# logo

graphics.set_font("bitmap3x5")
TITLE_WIDTH = graphics.measure_text("nintomdo", scale=1, fixed_width=True)
for tx in range(-16, TITLE_WIDTH + 16, 1):
    graphics.set_pen(screen.PALETTE.black)
    graphics.clear()
    graphics.set_pen(screen.PALETTE.red)
    graphics.text("nintomdo", -tx, 1, scale=1, fixed_width=True)
    graphics.set_pen(screen.PALETTE.white)
    graphics.text("game-guy", -tx, 8, scale=1, fixed_width=True)
    stellar.update(graphics)
    time.sleep_ms(25)

# calibrate input

msa_input.msa_input_init()

# timer
FPS = 30
DT_MS = round(1000/FPS)

# selection screen

GAME = None
while True:
    # note that import is relative to main.py in root
    if DEBUG_MODE == 1 or stellar.is_pressed(StellarUnicorn.SWITCH_A):
        import breakout as GAME
    if DEBUG_MODE == 2 or stellar.is_pressed(StellarUnicorn.SWITCH_B):
        import tetris as GAME
    if DEBUG_MODE == 3 or stellar.is_pressed(StellarUnicorn.SWITCH_C):
        import snake as GAME
    if DEBUG_MODE == -1:
        GAME = screen
    if DEBUG_MODE == -2:
        import input_test as GAME

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
    GAME.update(DT_MS / 1000)

    graphics.set_pen(screen.PALETTE.black)
    graphics.clear()
    GAME.draw(graphics)

    stellar.update(graphics)

    time.sleep_ms(DT_MS)
