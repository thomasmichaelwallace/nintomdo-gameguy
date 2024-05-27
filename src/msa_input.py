import math
import time
from pimoroni_i2c import PimoroniI2C
from breakout_msa311 import BreakoutMSA311

print("DEBUG_MSA_04")

PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
msa = BreakoutMSA311(i2c)

INPUT_DEAD_ZONE = 0.2
INPUT_MAX_ZONE = 0.5

INPUT_ZERO = 0
CALIBRATION_LIMIT = 0.2 # exclude values outside of this limit when calibrating

PRINT_DEBUG = False

def debug_print(*args):
    if PRINT_DEBUG:
        print(*args)

def msa_input_init():
    global INPUT_ZERO # pylint: disable=global-statement
    print("staring calibration [hold]")
    readings = [0.0]
    time.sleep_ms(1000) # wait for sensor to settle
    print("calibrating...")
    for _ in range(100):
        x = msa.get_x_axis()
        if abs(x) < CALIBRATION_LIMIT:
            readings.append(x)
        else:
            print("skipped", x)
    INPUT_ZERO = sum(readings) / len(readings)
    print("calibrated", INPUT_ZERO)
    time.sleep_ms(250) # allow me to read this

def get_tilt_float() -> float:
    raw_x = msa.get_x_axis()
    input_x = raw_x - INPUT_ZERO
    unsigned_x = abs(input_x) - INPUT_DEAD_ZONE
    if unsigned_x <= 0:
        return 0 # ensure dead zone is exactly zero
    clamp_norm_x = min(unsigned_x, INPUT_MAX_ZONE) / INPUT_MAX_ZONE
    float_x = -math.copysign(clamp_norm_x, input_x) # x is inverted
    debug_print("raw_x", raw_x, "float_x", float_x)
    return float_x

LAST_TILT_BUTTON = 0

def get_tilt_as_button() -> int:
    global LAST_TILT_BUTTON # pylint: disable=global-statement
    input_x = get_tilt_float()
    if input_x < 0 and LAST_TILT_BUTTON != -1:
        LAST_TILT_BUTTON = -1
        return -1
    if input_x > 0 and LAST_TILT_BUTTON != 1:
        LAST_TILT_BUTTON = 1
        return 1
    if input_x == 0:
        LAST_TILT_BUTTON = 0
    return 0

T = 0
JUMP_INTERRUPT = False
JUMP_VELOCITY = 0
JUMP_COOLDOWN_INTERVAL = 1.0

def get_jump() -> bool:
    global JUMP_INTERRUPT, T # pylint: disable=global-statement
    if JUMP_INTERRUPT:
        debug_print("jump!", JUMP_VELOCITY)
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
