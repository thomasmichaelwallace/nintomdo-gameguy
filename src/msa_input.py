import math
from pimoroni_i2c import PimoroniI2C
from breakout_msa311 import BreakoutMSA311

print("DEBUG_MSA_020")

PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
msa = BreakoutMSA311(i2c)

PRINT_DEBUG = False

def debug_print(*args):
    if PRINT_DEBUG:
        print(*args)

INPUT_DEAD_ZONE = 0.3 # 0.2-0.5 if top of shirt
INPUT_MAX_ZONE = 0.6

INPUT_ZERO = 0
CALIBRATION_LIMIT = 0.2 # exclude values outside of this limit when calibrating

def msa_input_init():
    global INPUT_ZERO # pylint: disable=global-statement
    print("staring calibration [hold]")
    readings = [0.0]
    print("calibrating...")
    for _ in range(100):
        x = msa.get_x_axis()
        if abs(x) < CALIBRATION_LIMIT:
            readings.append(x)
        else:
            print("skipped", x)
    INPUT_ZERO = sum(readings) / len(readings)
    print("calibrated", INPUT_ZERO)

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
LAST_TILT_DEBOUNCE = 0

LAST_TILT_TICKING_BUTTON = 0
LAST_TILT_TICKING_DEBOUNCE = 0
TICKING_BUTTON_TIMER = 0
FASTEST_TICK = 0.20
SLOWEST_TICK = 0.75

DEBOUNCE_INTERVAL = FASTEST_TICK

# returns (has changed, value, debounce_time)
def _get_debounced_button(input_x, last, t):
    if input_x < 0:
        next_button = -1
    elif input_x > 0:
        next_button = 1
    else:
        next_button = 0

    if next_button == last:
        # no change
        return (False, 0, DEBOUNCE_INTERVAL)

    if last in (0, -next_button):
        # moving out from zero or very quickly from left/right
        # reset debounce
        debug_print("button press", next_button)
        return (True, next_button, DEBOUNCE_INTERVAL)

    # moving back to zero requires debounce
    if t <= 0:
        debug_print("button zero", next_button)
        return (True, 0, DEBOUNCE_INTERVAL)

    debug_print("debounce", t)
    return (False, 0, t)

def get_tilt_as_button(dt) -> int:
    global LAST_TILT_BUTTON, LAST_TILT_DEBOUNCE # pylint: disable=global-statement
    input_x = get_tilt_float()
    LAST_TILT_DEBOUNCE -= dt
    update, value, debounce_timer = _get_debounced_button(
        input_x, LAST_TILT_BUTTON, LAST_TILT_DEBOUNCE
    )
    LAST_TILT_DEBOUNCE = debounce_timer
    if update:
        LAST_TILT_BUTTON = value
    return value


def get_tilt_as_ticking_button(dt) -> int:
    global LAST_TILT_TICKING_BUTTON, LAST_TILT_TICKING_DEBOUNCE, TICKING_BUTTON_TIMER # pylint: disable=global-statement
    input_x = get_tilt_float()
    LAST_TILT_TICKING_DEBOUNCE -= dt
    update, value, debounce_timer = _get_debounced_button(
        input_x, LAST_TILT_TICKING_BUTTON, LAST_TILT_TICKING_DEBOUNCE
    )
    LAST_TILT_TICKING_DEBOUNCE = debounce_timer

    if LAST_TILT_TICKING_BUTTON != 0:
        TICKING_BUTTON_TIMER += dt
        tick_threshold = SLOWEST_TICK - (SLOWEST_TICK - FASTEST_TICK) * abs(input_x)
        if TICKING_BUTTON_TIMER > tick_threshold:
            debug_print("resetting button")
            LAST_TILT_TICKING_BUTTON = 0
            TICKING_BUTTON_TIMER = 0

    if update:
        LAST_TILT_TICKING_BUTTON = value
        TICKING_BUTTON_TIMER = 0
    return value

JUMP_VELOCITY = 0
JUMP_COOLDOWN_INTERVAL = 0.5 # 0.3 if top of shirt
JUMP_G_THRESHOLD = 1.95 # 1.9 if top of shirt
JUMP_STATE = 0
JUMP_COOLDOWN_TIMER = 0

def get_jump(dt) -> bool: # pylint: disable=too-many-return-statements
    global JUMP_STATE, JUMP_VELOCITY, JUMP_COOLDOWN_TIMER # pylint: disable=global-statement

    y = msa.get_y_axis()
    if JUMP_STATE == 0: # ready for jump
        if y > JUMP_G_THRESHOLD:
            debug_print("start jump", y)
            JUMP_VELOCITY = y
            JUMP_STATE = 1
            return True
        return False

    if JUMP_STATE == 1: # jump in progress
        JUMP_VELOCITY = max(JUMP_VELOCITY, y)
        if y < JUMP_G_THRESHOLD:
            JUMP_STATE = 2
            JUMP_COOLDOWN_TIMER = JUMP_COOLDOWN_INTERVAL
        return False

    # start/run timer to skip next two states
    JUMP_COOLDOWN_TIMER -= dt
    if JUMP_COOLDOWN_TIMER <= 0:
        debug_print("end jump as cooldown", y, JUMP_VELOCITY)
        JUMP_STATE = 0
        return False

    if JUMP_STATE == 2: # jump might be complete, but maybe waiting for rebound
        debug_print("rebound check", y, JUMP_VELOCITY)
        if y > JUMP_G_THRESHOLD:
            debug_print("rebound", y, JUMP_VELOCITY)
            JUMP_STATE = 3
            JUMP_COOLDOWN_TIMER = JUMP_COOLDOWN_INTERVAL # reset-timer
        return False

    if JUMP_STATE == 3: # rebound in progress
        if y < JUMP_G_THRESHOLD:
            debug_print("rebound ended", y, JUMP_VELOCITY)
            JUMP_STATE = 0 # short-circuit timer
        return False

    print("jump_state_error", JUMP_STATE)
    return False
