from gpiozero import Button, LED
from signal import pause
import neopixel
import board
import time
import sys
import signal
import colorsys
import math
import pygame
import gif_pygame as gifpy
from pygame.locals import *

# ~ button init
hit_button = Button(4, bounce_time=0.05)
select_button = Button(3, bounce_time=0.05)
pixel_pin = board.D18
select_button.hold_time = 5
press_print=None
do_slide =False
do_eject=False
# ~ global var init
press_count = 0
x=0
y=0
screen_w = 1920
screen_h = 1080

# ~ pygame init
pygame.init()
screen = pygame.display.set_mode((screen_w,screen_h))
running=True

#pygame sounds
yes_sound = pygame.mixer.Sound("yes.mp3")
no_sound = pygame.mixer.Sound("no.mp3")

# ~ init logo load
screen.fill("black")
image = pygame.image.load("images/logo.tiff")
image = pygame.transform.scale(image,(screen_w,screen_h))

good_gif = gifpy.load("yes.gif")
scaledframes = [
    (pygame.transform.scale(frame, (screen_w,screen_h)), duration)
    for frame, duration in good_gif.frames
]

good_fullscreen_gif = gifpy.GIFPygame(scaledframes)

bad_gif = gifpy.load("nope.gif")
scaledframes_nope = [
        (pygame.transform.scale(frame, (screen_w,screen_h)), duration)
        for frame, duration in bad_gif.frames
]

bad_fullscreen_gif = gifpy.GIFPygame(scaledframes_nope)
screen.blit(image,(x,y))


# ~ LED init
led_on = False
num_pixels = 240
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=True, pixel_order=ORDER)

########## Hammers ###########

red_hammer = Button(6, pull_up=True, bounce_time=0.2)
green_hammer = Button(19, pull_up=True, bounce_time=0.2)
purple_hammer = Button(13, pull_up=True, bounce_time=0.2)

def check_initial_hammer():
    global current_hammer
    if red_hammer.is_pressed:
        current_hammer = 1
        print("Hammer 1 (red) plugged in at startup.")
    elif green_hammer.is_pressed:
        current_hammer = 2
        print("Hammer 2 (green) plugged in at startup.")
    elif purple_hammer.is_pressed:
        current_hammer = 3
        print("Hammer 3 (purple) plugged in at startup.")
    else:
        current_hammer = None
        print("No hammer plugged in at startup.")

# After hammer button definitions:
check_initial_hammer()


def hammer_handler(hammer_colour):
    def plugged_in():
        global current_hammer
        current_hammer = hammer_colour
        print(f"Hammer {hammer_colour} plugged in.")
    return plugged_in

def hammer_handler_unplugged(hammer_colour):
    def unplugged():
        global current_hammer
        if current_hammer == hammer_colour:
            current_hammer = None
        print(f"Hammer {hammer_colour} unplugged.")
    return unplugged


def presses():
    # ~ select material for button presses
    global press_count, press_print,image, do_slide
    do_slide = True
    press_count += 1
    pixels.fill((0,0,0))

    if press_count % 3 == 0:
        press_print = "Cesium"

    elif press_count % 3 == 1:
        press_print="Potassium"

    elif press_count % 3 == 2:
        press_print="Cerium"

    print(press_print)

def image_update():
    global image, x,y, press_count,do_slide

    slide(image)

    do_slide = False

    if press_count % 3 == 0:
        image = pygame.image.load("images/Cs.jpeg")

    elif press_count % 3 == 1:
        image = pygame.image.load("images/K.jpeg")

    elif press_count % 3 == 2:
        image = pygame.image.load("images/Ce.jpeg")

    image = pygame.transform.scale(image,(screen_w,screen_h))

    screen.blit(image,(0,0))
    pygame.display.flip()


def slide(image):
    global x,y
    for _ in range(95):
        x+=20
        screen.blit(image,(x,y))
        pygame.display.flip()
    x=0
    y=0

def eject(fullscreen_gif):
    global do_eject
    clock=pygame.time.Clock()

    for frame, duration in fullscreen_gif.frames:
        screen.blit(frame, (0,0))
        pygame.display.flip()
        pygame.time.delay(int(duration * 1000))
#    fullscreen_gif.render(screen,(0,0))
    
    sound.play()
    do_eject = False


def shutdown_handler(sig=None, frame=None):
    print("\nExiting... Turning off LEDs.")
    pixels.fill((0, 0, 0))
    hit_button.close()
    select_button.close()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

def hit_action():
    global press_print, led_on, do_eject, current_hammer, percent, fullscreen_gif

    if press_print==None:
        return


    if current_hammer == 1:
        hammer_name = "Red Hammer"
        hammer_freq = 1.95
    elif current_hammer == 2:
        hammer_name = "Green Hammer"
        hammer_freq = 2.29
    elif current_hammer == 3:
        hammer_name = "Purple Hammer"
        hammer_freq= 2.90
    else:
        hammer_name = "No hammer detected"
        hammer_freq = 0.000000001

    if press_print == "Cesium":
        freq_threshold = 1.95
        print("Cesium selected. LEDs on.")
    elif press_print == "Potassium":
        freq_threshold = 2.29
        print("Potassium selected. LEDs on.")
    elif press_print == "Cerium":
        freq_threshold = 2.90
        print("Cerium selected. LEDs on.")

    percent = min(hammer_freq / freq_threshold, 1.0)
    print(f"Last button state: {press_print} and threshold {freq_threshold} and hammer {hammer_freq}")

    animate_LEDs(duration=3, fps=30)

    if percent == 1.0:
        fullscreen_gif =  good_fullscreen_gif
        sound = yes_sound
        do_eject = True
    else:
        fullscreen_gif = bad_fullscreen_gif
        sound = no_sound
        do_eject = True


def animate_LEDs(duration=3, fps=30):
    global percent
    strand_len = num_pixels // 4
#    total_steps = strand_len
#    delay = duration / total_steps
    max_lit = max(2, int(strand_len * percent))
    delay = duration / max_lit

    pixels.fill((0, 0, 0))  # clear all LEDs at start
    step_increment = 2

    for step in range(0, max_lit, step_increment):
        for strand in range(4):
            offset = strand * strand_len
            reverse = (strand % 2 == 1)

            for led_step in range(step, min(step + step_increment, max_lit)):
                hue = led_step / max(max_lit - 1, 1)
                r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                color = (int(r * 255), int(g * 255), int(b * 255))

                if reverse:
                    pixel_index = offset + strand_len - 1 - led_step
                else:
                    pixel_index = offset + led_step

                pixels[pixel_index] = color

        pixels.show()
        time.sleep(delay)

print("Ready. Press the button.")


# ~ PyGame loop
while running:
    hit_button.when_pressed = hit_action
    select_button.when_pressed = presses

    red_hammer.when_pressed = hammer_handler(1)
    red_hammer.when_released = hammer_handler_unplugged(1)

    green_hammer.when_pressed = hammer_handler(2)
    green_hammer.when_released = hammer_handler_unplugged(2)

    purple_hammer.when_pressed = hammer_handler(3)
    purple_hammer.when_released = hammer_handler_unplugged(3)



    if do_slide:
        image_update()
    if do_eject:
        eject(fullscreen_gif)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            shutdown_handler(None, None)
        if event.type == pygame.KEYDOWN:
            presses()

    pygame.display.flip()
