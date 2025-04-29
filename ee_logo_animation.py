import pygame
from gpiozero import Button, LED
from signal import pause

pygame.init()
screen = pygame.display.set_mode((1280,720))
#clock = pygame.time.Clock()
running = True
x = 0
y = 0
hit_button = Button(4, bounce_time=0.05)

def press():
    global x, y
    x+=50
    print(f"x={x}, y={y}")
    screen.blit(logo, (x, y))



#Puts up EE logo and fits to screen size
screen.fill("black")
logo = pygame.image.load('logo.tiff')
logo = pygame.transform.scale(logo, (1280, 720))

while running:
 
    screen.blit(logo, (x, y))

       
    hit_button.when_pressed = press
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    



    pygame.display.flip()


#clock.tick(60)
    
pygame.quit()