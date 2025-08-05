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

### button initialization
hit_button = Button(4, bounce_time=0.05)
select_button = Button(3, bounce_time=0.05)
pixel_pin = board.D18
press_print=None
### global var init for button
press_count = 0

### animation initialization
do_slide =False
do_eject=False
### global var init for pygame
x=0
y=0
clock=pygame.time.Clock()
screen_w = 1920
screen_h = 1080
clock.tick(60)

### runs pygame start screen and LED reset
def main():
    global screen, running, image, pixels, led_on, num_pixels, ORDER
    pygame.init()
    screen = pygame.display.set_mode((1920,1080))
    running=True
### Load electron ejector logo
    screen.fill("black")
    image = pygame.image.load("images/logo.png")
    image = pygame.transform.scale(image,(1920,1080))
    screen.blit(image,(x,y))
### LED initialization fill all black 
    led_on = False
    num_pixels = 240
    ORDER = neopixel.GRB
    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=True, pixel_order=ORDER)
    pixels.fill((0, 0, 0))

main()

### pygame load sounds 
yes_sound = pygame.mixer.Sound("yes.mp3")
no_sound = pygame.mixer.Sound("no.mp3")


### pygame load gifs/animations 
good_gif = gifpy.load("yes.gif", loops=1)
scaledframes = [
    (pygame.transform.scale(frame, (screen_w,screen_h)), duration)
    for frame, duration in good_gif.frames
]
good_fullscreen_gif = gifpy.GIFPygame(scaledframes)

bad_gif = gifpy.load("nope.gif", loops=1)
scaledframes_nope = [
        (pygame.transform.scale(frame, (screen_w,screen_h)), duration)
        for frame, duration in bad_gif.frames
]
bad_fullscreen_gif = gifpy.GIFPygame(scaledframes_nope)

### Hammer set up
red_hammer = Button(6, pull_up=True, bounce_time=0.2)
green_hammer = Button(19, pull_up=True, bounce_time=0.2)
purple_hammer = Button(13, pull_up=True, bounce_time=0.2)

### Hammer initial function - detects on start-up
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

check_initial_hammer()

### Function for hammer plugged in or unplugged
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

### Select button, determines what materials Cs, K, Ce are shown 
def presses():
    global press_count, press_print,image, do_slide, do_eject
    do_eject = False
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

### Runs select animation to run through material character screens
def image_update():
    global image, x,y, press_count,do_slide

    slide(image)

    do_slide = False

    if press_count % 3 == 0:
        image = pygame.image.load("Cs.png")

    elif press_count % 3 == 1:
        image = pygame.image.load("K.png")

    elif press_count % 3 == 2:
        image = pygame.image.load("Ce.png")

    image = pygame.transform.scale(image,(screen_w,screen_h))

    screen.blit(image,(0,0))
    pygame.display.flip()

### Actual slide animation for switching material screens
def slide(image):
    global x,y
    for _ in range(95):
        x+=screen_w / 30
        screen.blit(image,(x,y))
        pygame.display.flip()
    x=0
    y=0

### Animation for eject outcome, plays gif and sound 
def eject(fullscreen_gif):
    global do_eject
    sound.play()

    for _ in range(1):
        for frame, duration in fullscreen_gif.frames:
            screen.blit(frame, (0,0))
            pygame.display.flip()
            pygame.time.delay(int(duration * 0.5))
#    fullscreen_gif.render(screen,(0,0))
    do_eject = False

### Shutdown handler, makes sure GPIO does not hang-up and LEDs are reset when exiting
def shutdown_handler(sig=None, frame=None):
    print("\nExiting... Turning off LEDs.")
    pixels.fill((0, 0, 0))
    hit_button.close()
    select_button.close()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

### Hit button actions
def hit_action():
    global press_print, led_on, do_eject, current_hammer, percent, fullscreen_gif, sound

### Checks if select has been pressed
    if press_print==None:
        return
### Checks the plugged-in hammer and sets threshold frequency of hammer
    if current_hammer == 1:
        hammer_name = "Red Hammer"
        #hammer_freq = 1.95
        hammer_freq = 1.00
    elif current_hammer == 2:
        hammer_name = "Green Hammer"
        #hammer_freq = 2.29
        hammer_freq = 2
    elif current_hammer == 3:
        hammer_name = "Purple Hammer"
        #hammer_freq= 2.90
        hammer_freq= 3
    else:
        hammer_name = "No hammer detected"
        hammer_freq = 0.000000001
### Reads material, sets threshold frequency of material
    
    if press_print == "Cesium":
        #freq_threshold = 1.95
        freq_threshold = 1
        print("Cesium selected. LEDs on.")
    elif press_print == "Potassium":
        #freq_threshold = 2.29
        freq_threshold = 2.00
        print("Potassium selected. LEDs on.")
    elif press_print == "Cerium":
        #freq_threshold = 2.90
        freq_threshold = 3.00
        print("Cerium selected. LEDs on.")

### Compares hammer frequency with threshold frequency of material, produces animation and sounds and LED light up based on outcome yes or no    
    percent = min(hammer_freq / freq_threshold, 1.0)
    print(f"Last button state: {press_print} and threshold {freq_threshold} and hammer {hammer_freq}")

    animate_LEDs(duration=3, fps=30)

    if percent == 1.0:
        sound = yes_sound
        fullscreen_gif =  good_fullscreen_gif
        do_eject = True
    else:
        sound = no_sound
        fullscreen_gif = bad_fullscreen_gif
        do_eject = True

### LED animation, 4 strings in sequence folded back on itself, light up in rainbow and slowly ascend 
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
                    pixel_index = offset + led_step
                else:
                    pixel_index = offset + strand_len - 1 - led_step

                pixels[pixel_index] = color

        pixels.show()
        time.sleep(delay)

print("Ready. Press the button.")


### Soft reset with keyboard press to title electron ejector screen
def soft_reset():
    main()

### PyGame loop runs the main software based on button presses and hammers
while running:
    #time.sleep(0.001)
    hit_button.when_released = hit_action
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
            soft_reset()

    pygame.display.flip()
