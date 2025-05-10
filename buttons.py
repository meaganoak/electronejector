from gpiozero import Button, LED
from signal import pause
import neopixel
import board
import time
import sys
import signal
import colorsys
import math

hit_button = Button(4, bounce_time=0.05)
#select_button = Button(3, bounce_time=0.05)
#press_count = 0
#press_print = ""
press_print = "Cerium"


led_on = False
pixel_pin = board.D18
num_pixels = 240
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=True, pixel_order=ORDER)


#def presses():
#    global press_count, press_print
#    press_count = (press_count % 3) + 1
#
#    if press_count == 1:
#        press_print = "Cesium"
#    if press_count == 2:
#        press_print="Potassium"
#    if press_count == 3:
#        press_print="Cerium"

#    print(press_print)

def shutdown_handler(sig, frame):
    print("\nExiting... Turning off LEDs.")
    pixels.fill((0, 0, 0))
    hit_button.close()
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

# --- Main Action ---
def hit_action():
    global press_print, led_on

    if press_print == "Cesium":
        freq_threshold = 1.95
        percent = freq_threshold / 2.90
        print("Cesium selected. LEDs on.")
    elif press_print == "Potassium":
        freq_threshold = 2.29
        percent = freq_threshold / 2.90
        print("Potassium selected. LEDs on.")
    elif press_print == "Cerium":
        freq_threshold = 2.90
        percent = freq_threshold / 2.90
        print("Cerium selected. LEDs on.")

    print(f"Last button state: {press_print} and threshold {freq_threshold}")

    active_pixels = int((num_pixels // 2) * percent)
    for i in range(active_pixels):
        hue = i / active_pixels  
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        color = (int(r * 255), int(g * 255), int(b * 255))

        pixels[i] = color
        pixels[num_pixels - 1 - i] = color

    for i in range(active_pixels, num_pixels // 2):
        pixels[i] = (0, 0, 0)
        pixels[num_pixels - 1 - i] = (0, 0, 0)

    led_on = True

hit_button.when_pressed = hit_action

print("Ready. Press the button.")
try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    shutdown_handler(None, None)
