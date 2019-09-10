import bhi160
import utime
import display
import vibra
import buttons
import math

fov = 45  # field of vision in degrees
freq = 0.2  # how often to measure, in seconds

center = (80, 40)
radius = 30

orientation = bhi160.BHI160Orientation()
disp = display.open()


def draw_compass(relative_north, color):
    disp.clear()
    for ii in range(30):
        disp.pixel(
            int(center[0] + radius * math.cos(math.radians(12 * ii))),
            int(center[1] + radius * math.sin(math.radians(12 * ii))),
            col=(100, 100, 100),
        )
    angle = math.radians(relative_north) - math.pi / 2
    disp.circ(
        int(center[0] + radius * math.cos(angle)),
        int(center[1] + radius * math.sin(angle)),
        5,
        col=color,
    )
    disp.line(
        int(center[0]),
        int(center[1] - 0.8 * radius),
        int(center[0]),
        int(center[1] - 1.2 * radius),
        col=(100, 100, 100),
        size=1,
    )
    disp.update()


while True:
    samples = orientation.read()
    if len(samples) == 0:
        utime.sleep(freq)
        continue
    sample = samples[0]

    # I *think* status == 3 is good.
    degrees = sample.x
    color = [255, 0, 0]
    if sample.status == 1:
        color = [255, 128, 0]
    elif sample.status == 2:
        color = [255, 255, 0]
    elif sample.status == 3:
        color = [0, 200, 0]

    draw_compass(-degrees, color)

    if sample.status == 3:
        pointing_north = degrees > 360 - fov / 2 or degrees < fov / 2
        vibra.set(pointing_north)
        utime.sleep(freq / 2)
        vibra.set(False)
        utime.sleep(freq / 2)
    else:
        utime.sleep(freq)

    # Check for button presses.
    v = buttons.read(buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT | buttons.TOP_RIGHT)
    button_pressed = v != 0
    if button_pressed and v & buttons.BOTTOM_LEFT != 0:
        freq *= 1 / 1.2
    elif button_pressed and v & buttons.BOTTOM_RIGHT != 0:
        freq *= 1.2
    elif button_pressed and v & buttons.TOP_RIGHT != 0:
        pass
