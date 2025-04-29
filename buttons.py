from gpiozero import Button, LED
from signal import pause


hit_button = Button(4, bounce_time=0.05)
select_button = Button(3, bounce_time=0.05)

press_count = 0
press_print = ""

def presses():
    global press_count, press_print
    press_count = (press_count % 3) + 1
    
    if press_count == 1:
        press_print = "Sodium"
    if press_count == 2:
        press_print="Potassium"
    if press_count == 3:
        press_print="Magnesium"

    print(press_print)
 

def hit_action():
    if press_print == "Sodium":
         freq_threshold = "25"
    elif press_print == "Potassium":
         freq_threshold = "50"
    elif press_print == "Magnesium":
         freq_threshold = "100"         
    print(f"Last button state: {press_print} and {freq_threshold}")




select_button.when_pressed = presses
hit_button.when_pressed = hit_action


pause()