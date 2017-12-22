import resources.Equipment.PressureEquipment as pEquip

# Import a library of functions called 'pygame'
import pygame
from math import pi

# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the height and width of the screen
size = [600, 600]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Example code for the draw module")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

pGuage = pEquip.PressureGauge(100,150,100,90)
thermometer = pEquip.Thermometer(300,300,350,20)

equipment = pygame.sprite.Group()
equipment.add(pGuage)
equipment.add(thermometer)

pressure = 90
temp = 20
goingUp = True

while not done:

    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(10)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # All drawing code happens after the for loop and but
    # inside the main while done==False loop.

    # Clear the screen and set the screen background
    screen.fill(WHITE)

    equipment.draw(screen)
    pGuage.drawPointer(screen,pressure)
    pressure += 1
    thermometer.drawMarker(screen, temp)
    print(temp)
    if temp == thermometer.minTemp:
        goingUp = True
    elif temp == thermometer.maxTemp:
        goingUp = False

    if goingUp:
        temp += 5
    else:
        temp -= 5


    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()