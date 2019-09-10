import bhi160
import utime
import display
import vibra
import buttons

fov = 45 # field of vision in degrees
freq = 0.2 # second

orientation = bhi160.BHI160Orientation()
disp = display.open()

while True:
    samples = orientation.read()

    if len(samples) > 0:
        sample = samples[0]

        degrees = sample.x

        color = [255, 0, 0]
        if sample.status == 1:
            color = [255, 128, 0]
        elif sample.status == 2:
            color = [255, 255, 0]
        elif sample.status == 3:
            color = [0, 200, 0]

        disp.clear()
        disp.print("%f" % degrees, posy = 20, fg = color)
        disp.print("%f" % freq, posy = 40)
        disp.update()

        if sample.status == 3:
            pointing_north = degrees > 360-fov/2 or degrees < fov/2
            vibra.set(pointing_north)
            utime.sleep(freq/2)
            vibra.set(False)
            utime.sleep(freq/2)
        else:
            utime.sleep(freq)
    else:
        utime.sleep(freq)

    # check for button presses
    v = buttons.read(
        buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT | buttons.TOP_RIGHT
    )
    button_pressed = v != 0
    if button_pressed and v & buttons.BOTTOM_LEFT != 0:
        freq -= 0.05
        pass
    elif button_pressed and v & buttons.BOTTOM_RIGHT != 0:
        freq += 0.05
        pass
    elif button_pressed and v & buttons.TOP_RIGHT != 0:
        pass
