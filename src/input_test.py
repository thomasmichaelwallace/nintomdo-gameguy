from picographics import PicoGraphics
import msa_input
import screen

print("DEBUG_10")

def init():
    pass

TILT_X = 8
TILT_DIR = 0 # -1 left, 0, 1 right

SHOW_JUMP_FOR = 0.2 # how long to show jump
SHOW_JUMP = False
JUMP_TIMER = 0

def update(dt):
    global JUMP_TIMER, SHOW_JUMP, TILT_X, TILT_DIR # pylint: disable=global-statement

    # get_tilt_float
    tilt_float = msa_input.get_tilt_float()
    print("get_tilt_float:", tilt_float)
    TILT_X = max(min(int(tilt_float * 8) + 8, screen.WIDTH - 1), 0)
    if tilt_float == 0:
        TILT_DIR = 0
    elif tilt_float < 0:
        TILT_DIR = -1
    else:
        TILT_DIR = 1

    # get jump
    if msa_input.get_jump():
        print("jump!")
        SHOW_JUMP = True
        JUMP_TIMER = SHOW_JUMP_FOR
    if JUMP_TIMER > 0:
        JUMP_TIMER -= dt
        if JUMP_TIMER <= 0:
            SHOW_JUMP = False

def draw(graphics: PicoGraphics):
    graphics.set_pen(screen.PALETTE.blue)
    graphics.pixel(TILT_X, 8)

    graphics.set_pen(screen.PALETTE.green)
    if TILT_DIR == 0:
        graphics.pixel(TILT_X, 6)
    elif TILT_DIR == -1:
        graphics.pixel(0, 6)
    else:
        graphics.pixel(screen.WIDTH - 1, 6)

    if SHOW_JUMP:
        graphics.set_pen(screen.PALETTE.red)
        graphics.rectangle(1, 1, 2, 2)
