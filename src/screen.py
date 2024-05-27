import math
from picographics import PicoGraphics
from stellar import StellarUnicorn

print("DEBUG_21")

WIDTH = StellarUnicorn.WIDTH
HEIGHT = StellarUnicorn.HEIGHT

# palette will be defined as pens on init()
class _Pallet(): # pylint: disable=too-few-public-methods
    red = 1
    orange = 2
    yellow = 3
    spring_green = 4
    green = 5
    cyan = 6
    light_blue = 7
    azure = 8
    blue = 9
    indigo = 10
    purple = 11
    pink = 12
    dark_red = 13
    dark_orange = 14
    dark_green = 15
    dark_blue = 16
    dark_purple = 17
    white = int(18)
    black = int(19)

PALETTE = _Pallet()

# define colours relative to reference image shown in test:
# top-left origin 1-based row, column references for each colour
REFS = {
    # == brightest columns ==
    "red": [1, 1],
    "orange": [1,2],
    "yellow": [1,3],
    "spring_green": [1,4],
    # 5-7 are all nearly identical shades of green
    "green": [1, 6],
    "cyan": [1, 8],
    "light_blue": [16, 9],
    "azure": [1, 10],
    # 11-12 are nearly identical shades of blue
    "blue": [16, 12],
    # 13 is indistinct due to lack of blend
    "indigo": [16, 14],
    "purple": [10, 13],
    "pink": [10, 16],
    # == dark variants ==
    "dark_red": [14, 1],
    "dark_orange": [15, 2],
    # yellow and spring green do not have dark variants
    "dark_green": [11, 6],
    # cyan and light blue do not have dark variants
    "dark_blue": [1, 12],
    "dark_purple": [1, 13],
}

def from_hsv(h, s, v): # pylint: disable=too-many-return-statements
    i = math.floor(h * 6.0)
    f = h * 6.0 - i
    v *= 255.0
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)

    i = int(i) % 6
    if i == 0:
        return int(v), int(t), int(p)
    if i == 1:
        return int(q), int(v), int(p)
    if i == 2:
        return int(p), int(v), int(t)
    if i == 3:
        return int(p), int(q), int(v)
    if i == 4:
        return int(t), int(p), int(v)
    if i == 5:
        return int(v), int(p), int(q)
    return 0, 0, 0 # should never happen

def screen_init(graphics: PicoGraphics):
    hue_map = [from_hsv(x / WIDTH, 1.0, 1.0) for x in range(WIDTH)]
    for key, ref in REFS.items():
        r, c = ref
        x, y = c - 1, r - 1
        colour = hue_map[x]
        v = (math.sin((x + y) / 3.0) + 1.5) / 2.5
        pen = graphics.create_pen(
            int(colour[0] * v), int(colour[1] * v), int(colour[2] * v)
        )
        setattr(PALETTE, key, pen)
    # standard pens
    PALETTE.black = graphics.create_pen(0, 0, 0)
    PALETTE.white = graphics.create_pen(255, 255, 255)

# provide game implementation to be loadable when testing

T = 0
SHOW_ALL=False

def init():
    pass

def update(dt):
    global T, SHOW_ALL # pylint: disable=global-statement
    T += dt
    if T > 4:
        T = 0
        SHOW_ALL = not SHOW_ALL


def draw(graphics: PicoGraphics):
    if SHOW_ALL:
        hue_map = [from_hsv(x / WIDTH, 1.0, 1.0) for x in range(WIDTH)]
        hue_offset = 0.0
        stripe_width = 3.0
        phase_percent = 0
        for x in range(WIDTH):
            colour = hue_map[int((x + (hue_offset * WIDTH)) % WIDTH)]
            for y in range(HEIGHT):
                v = (math.sin((x + y) / stripe_width + phase_percent) + 1.5) / 2.5
                pen = graphics.create_pen(
                    int(colour[0] * v), int(colour[1] * v), int(colour[2] * v)
                )
                graphics.set_pen(pen) # type: ignore
                graphics.pixel(x, y)
    else:
        for key, ref in REFS.items():
            r, c = ref
            x, y = c - 1, r - 1
            pen = getattr(PALETTE, key)
            graphics.set_pen(pen)
            graphics.pixel(x, y)
