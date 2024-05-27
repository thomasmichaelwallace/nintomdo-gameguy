from picographics import PicoGraphics
import msa_input
import screen

print("DEBUG_44")

def init():
    msa_input.PRINT_DEBUG = True

TILT_X0 = 8
TILT_DIR = 0 # -1 left, 0, 1 right

SHOW_TILT_BUTTON_FOR = 0.2 # how long to show tilt button
SHOW_TILT_BUTTON = 0
TILT_BUTTON = 0 # -1 left, 0, 1 right
TILT_BUTTON_TIMER = 0

SHOW_JUMP_FOR = 0.2 # how long to show jump
SHOW_JUMP = False
JUMP_TIMER = 0

def update(dt):
    global TILT_X0, TILT_DIR, TILT_BUTTON, SHOW_TILT_BUTTON, TILT_BUTTON_TIMER # pylint: disable=global-statement
    global JUMP_TIMER, SHOW_JUMP # pylint: disable=global-statement

    # get_tilt_float
    tilt_float = msa_input.get_tilt_float()
    TILT_X0 = round((tilt_float * 7) + 7)
    if tilt_float == 0:
        TILT_DIR = 0
    elif tilt_float < 0:
        TILT_DIR = -1
    else:
        TILT_DIR = 1

    # get_tilt_as_button
    TILT_BUTTON = msa_input.get_tilt_as_button()
    if TILT_BUTTON != 0:
        SHOW_TILT_BUTTON = TILT_BUTTON
        TILT_BUTTON_TIMER = SHOW_TILT_BUTTON_FOR
    if TILT_BUTTON_TIMER > 0:
        TILT_BUTTON_TIMER -= dt
        if TILT_BUTTON_TIMER <= 0:
            SHOW_TILT_BUTTON = 0

    # get jump
    if msa_input.get_jump():
        SHOW_JUMP = True
        JUMP_TIMER = SHOW_JUMP_FOR
    if JUMP_TIMER > 0:
        JUMP_TIMER -= dt
        if JUMP_TIMER <= 0:
            SHOW_JUMP = False

def draw(graphics: PicoGraphics):
    # raw normalised tilt
    graphics.set_pen(screen.PALETTE.blue)
    graphics.rectangle(TILT_X0, 8, 2, 1)

    graphics.set_pen(screen.PALETTE.green)
    if TILT_DIR == -1:
        graphics.pixel(TILT_X0, 6)
    elif TILT_DIR == 1:
        graphics.pixel(TILT_X0 + 1, 6)

    graphics.set_pen(screen.PALETTE.orange)
    graphics.rectangle(7, 4, 2, 1)
    if SHOW_TILT_BUTTON == -1:
        graphics.pixel(5, 4)
    elif SHOW_TILT_BUTTON == 1:
        graphics.pixel(10, 4)

    if SHOW_JUMP:
        graphics.set_pen(screen.PALETTE.red)
        graphics.rectangle(1, 1, 2, 2)
