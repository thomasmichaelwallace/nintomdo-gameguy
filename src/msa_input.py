import math
from pimoroni_i2c import PimoroniI2C
from breakout_msa311 import BreakoutMSA311

PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
msa = BreakoutMSA311(i2c)

INPUT_MIN = 0.2
INPUT_MAX = 0.7

def get_tilt_float() -> float:
    input_x = -1 * msa.get_x_axis() # x axis is inverted
    print("input_x", input_x)
    clamp_x = max(min(abs(input_x), INPUT_MAX), INPUT_MIN) - INPUT_MIN
    return math.copysign(clamp_x, input_x) / (INPUT_MAX - INPUT_MIN)

T = 0
JUMP_INTERRUPT = False
JUMP_VELOCITY = 0
JUMP_COOLDOWN_INTERVAL = 1.0

def get_jump() -> bool:
    global JUMP_INTERRUPT, T # pylint: disable=global-statement
    if JUMP_INTERRUPT:
        print("jump!", JUMP_VELOCITY)
        JUMP_INTERRUPT = False
        T = -JUMP_COOLDOWN_INTERVAL
        return True
    return False

JUMP_G_THRESHOLD = 1.9

def update(dt):
    global T, JUMP_INTERRUPT, JUMP_VELOCITY # pylint: disable=global-statement
    y = msa.get_y_axis()
    T += dt
    if T > 0 and y > JUMP_G_THRESHOLD:
        JUMP_INTERRUPT = True
        JUMP_VELOCITY = max(JUMP_VELOCITY, y)
