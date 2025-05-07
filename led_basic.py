import neopixel
import board
import time
import sys

#This is a script that turns the LEDs on and red, and then elegantly terminates the program upon ctrl+c; the leds turn off first and gpio busy is avoided

pixel_pin = board.D18     # GPIO pin
num_pixels = 240          # Number of LEDs in your strip
ORDER = neopixel.GRB       

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=True, pixel_order=ORDER)

try:
    # Turn all pixels red as an example
    pixels.fill((255, 0, 0))
    print("LEDs on. Press Ctrl+C to turn them off and exit.")
    while True:
        time.sleep(1)  # keep the program running

except KeyboardInterrupt:
    print("\nCtrl+C detected. Turning off LEDs...")

finally:
    pixels.fill((0, 0, 0))  # Turn off all pixels
    print("LEDs off. Exiting.")
    sys.exit(0)
