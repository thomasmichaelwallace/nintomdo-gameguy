import time
from stellar import StellarUnicorn
from picographics import PicoGraphics, DISPLAY_STELLAR_UNICORN as DISPLAY
import msa_input
import screen

# global options

DEBUG_MODE=4
print("DEBUG_MODE:", DEBUG_MODE)
print("DEBUG_123")

# start screen
stellar = StellarUnicorn()
graphics = PicoGraphics(DISPLAY)
screen.screen_init(graphics)
BRIGHTNESS = 1
if DEBUG_MODE > 0:
    BRIGHTNESS = 1 # do not blind myself while working with the board directly
stellar.set_brightness(BRIGHTNESS)

# timer
FPS = 30
DT_MS = round(1000/FPS)

# logo

if DEBUG_MODE == 0:
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
        time.sleep_ms(DT_MS)

# calibrate input

msa_input.msa_input_init()

# selection screen

SELECTION=0
SELECTED=DEBUG_MODE
graphics.set_font("bitmap8")
while SELECTED == 0:
    if msa_input.get_jump(DT_MS / 1000):
        print("SELECTED:", SELECTED + 1)
        SELECTED = SELECTION + 1
        break

    INPUT_X = msa_input.get_tilt_as_button(DT_MS / 1000)
    if INPUT_X == 1:
        SELECTION = (SELECTION + 1) % 3
    if INPUT_X == -1:
        SELECTION = (SELECTION - 1) % 3

    graphics.set_pen(screen.PALETTE.black)
    graphics.clear()

    if SELECTION == 0:
        graphics.set_pen(screen.PALETTE.green)
        graphics.text("B", 4, 1)
    elif SELECTION == 1:
        graphics.set_pen(screen.PALETTE.red)
        graphics.text("T", 3, 1)
    elif SELECTION == 2:
        graphics.set_pen(screen.PALETTE.blue)
        graphics.text("S", 4, 1)
    else:
        graphics.set_pen(screen.PALETTE.white)
        graphics.text("?", 0, 1)

    stellar.update(graphics)

    time.sleep_ms(DT_MS)


GAME = None
# note that import is relative to main.py in root
if SELECTED == 1:
    import breakout as GAME
elif SELECTED == 2:
    import tetris as GAME
elif SELECTED == 3:
    import snake as GAME
elif SELECTED == 4:
    import runner as GAME
elif SELECTED == -2:
    import input_test as GAME
else:
    GAME = screen

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
