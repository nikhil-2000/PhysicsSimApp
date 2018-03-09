import resources.Equipment.SHCequipment as sEquip
from resources.Equipment.PressureEquipment import Thermometer
import resources.resourceManager as resM
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
size = [650, 400]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Example code for the draw module")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

equipment = pygame.sprite.Group()

block = sEquip.CopperBlock(100, 100, 400, 300)
block.insertThermometer()
block.insertHeater()

arrowGroup = pygame.sprite.Group()

nOfArrows = 7
spacing = 30
y = block.y
for i in range(nOfArrows):

    if i == nOfArrows-1:
        x = block.heaterBasePoint
        y += spacing
        angle = 90
    elif i % 2 == 0:
        x = block.heaterBasePoint - 40
        y += spacing
        angle = 0
    else:
        x = block.heaterBasePoint + 40
        angle = 180

    a = sEquip.HeatArrow(x,y,angle,2)
    arrowGroup.add(a)

equipment.add(block.heater)

temp = 20
alpha = 255
while not done:

    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(60)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # All drawing code happens after the for loop and but
    # inside the main while done==False loop.

    # Clear the screen and set the screen background
    screen.fill(WHITE)
    block.draw(screen)
    #block.thermometer.drawMarker(screen,temp)
    #if temp < 100: temp += 1

    for arrow in arrowGroup:
        arrow.fade()

    equipment.draw(screen)
    arrowGroup.draw(screen)



    #pygame.draw.line(screen, RED, block.thermometer.markerStart, block.thermometer.markerEnd, 10)


    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()