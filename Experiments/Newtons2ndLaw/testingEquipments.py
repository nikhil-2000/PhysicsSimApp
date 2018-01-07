
# Import a library of functions called 'pygame'
import pygame
import math
import resources.resourceManager as resM
import resources.Colour as cols

# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (91,68,68)
YELLOW = cols.YELLOW

class Cart(pygame.sprite.Sprite):
    def __init__(self,screen,bench):
        #Setting Attributes
        super(Cart, self).__init__()
        self.screen = screen
        img = pygame.image.load(resM.cartImg)
        self.image = pygame.transform.scale(img,(150,100))

        self.bench = bench                          #Needs Bench as reference point

        self.rect = self.image.get_rect()
        self.rect.left = self.bench.rect.left + 20  #Places cart relative to bench
        self.rect.bottom = self.bench.rect.top

        self.startCenter = self.rect.center         #Taken now to cart back to start Point

        self.noOfWeights = 0                        #Will determine speed

    def drawWeights(self):
        yCoord = self.rect.bottom - 48              #Marks start point of mass holder on cart
        for i in range(self.noOfWeights):
            weight = pygame.Surface((40, 10))       #The yellow part of the weight
            weight.fill(YELLOW)
            rect = weight.get_rect()                #Black outline of Weight
            rect.center = self.rect.centerx,yCoord
            self.screen.blit(weight,rect)           #Draw the Yellow surface
            pygame.draw.rect(self.screen,BLACK,rect,1)  #Draw Black Outline
            yCoord -= 10                            #Increment Y coord by weight height

class Bench(pygame.sprite.Sprite):
    def __init__(self,screen):
        #This Object is the table and fairly simple, it doesn't require any other methods
        #This acts as a reference point for:
            # The cart
            # The Pulley
            # The Dataloggers
        super(Bench, self).__init__()
        self.screen = screen
        self.image = pygame.Surface([450,70])
        self.image.fill(BROWN)

        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.bottom = 200

class Pulley():
    def __init__(self,screen,bench):
        #This will be a circle
        #The string will wrap around it
        self.radius = 15
        self.screen = screen
        self.bench = bench

        self.x = int(self.bench.rect.right + self.radius*math.cos(45))
        self.y = int(self.bench.rect.top - self.radius*math.sin(45))

        self.top = self.y - self.radius
        self.bottom = self.y + self.radius
        self.left = self.x - self.radius
        self.right = self.x + self.radius

    def draw(self):#Has to have a seperate draw function since it isn't a sprite
        pygame.draw.circle(self.screen,RED,(self.x,self.y),self.radius)

class MassHolder(pygame.sprite.Sprite):
    def __init__(self,screen,pulley):
        super(MassHolder, self).__init__()

        #This will have the masses which the cart doesn't have
        #Determines the speed of the cart
        img = pygame.image.load(resM.massHolderImg)
        self.image = pygame.transform.scale(img,(50,105))
        self.screen = screen

        self.pulley = pulley

        self.rect = self.image.get_rect()
        self.rect.centerx = self.pulley.x + self.pulley.radius
        self.rect.top = self.pulley.bench.rect.bottom

        self.noOfWeights = 5
        self.startCenter = self.rect.center
        self.time = 0


    def drawWeights(self):#Draws weights in a similair style to the cart
        yCoord = self.rect.bottom - 15
        for i in range(self.noOfWeights):
            weight = pygame.Surface((40, 10))
            weight.fill(YELLOW)
            rect = weight.get_rect()
            rect.center = self.rect.centerx,yCoord
            self.screen.blit(weight,rect)
            pygame.draw.rect(self.screen,BLACK,rect,1)
            yCoord -= 10

    def getSpeed(self):
        #This will accelerate the cart
        #I will generate these values more accurately in the real program
        #The aim of this was to get the cart accelerating depending on the weight
        self.time += 1
        return (self.noOfWeights/10) * self.time


class LightGate(pygame.sprite.Sprite):
    def __init__(self,screen,bench,lightGateNo):
        #This will record the velocity when cart passes by
        #More for show since I will be calculating the velocities at these points
        super(LightGate, self).__init__()

        self.screen = screen
        self.bench = bench

        image = pygame.image.load(resM.dataLoggerImg)
        self.image = pygame.transform.scale(image,(30,60))
        self.rect = self.image.get_rect()

        if lightGateNo == 1:#Decides whether it's the first of 2nd one
            self.rect.center = self.bench.rect.centerx,self.bench.rect.top
        else:
            self.rect.center = self.bench.rect.centerx + 150,self.bench.rect.top

    
def shift(cart,massHolder,speed):#Moves the cart by it's current speed
    cart.rect.x += speed
    massHolder.rect.y += speed
    return cart,massHolder

def switchWeights(cart,massHolder):#Takes a weight of the mass holder and moves it the cart
    massHolder.noOfWeights -= 1
    cart.noOfWeights += 1
    return cart,massHolder

# Set the height and width of the screen
size = [650, 400]
screen = pygame.display.set_mode(size)

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
isPaused = True

#Creating my Equipment
bench = Bench(screen)
cart = Cart(screen,bench)
pulley = Pulley(screen,bench)
massHolder = MassHolder(screen,pulley)
LG1 = LightGate(screen,bench,1)
LG2 = LightGate(screen,bench,2)

#Adding all sprite objects to group
equipment = pygame.sprite.Group()
equipment.add(bench)
equipment.add(cart)
equipment.add(massHolder)
equipment.add(LG1)
equipment.add(LG2)

button = pygame.Surface([100,20])
button.fill(cols.ORANGE)


while not done:

    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(10)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            print(mousePos)
            print("")
            bRect = button.get_rect()
            bRect.x,bRect.y = 100,300
            print(bRect.x)
            print(bRect.y)
            if bRect.collidepoint(mousePos):
                isPaused = not(isPaused)

    # All drawing code happens after the for loop and but
    # inside the main while done==False loop.

    # Clear the screen and set the screen background
    screen.fill(WHITE)      #Background

    pygame.draw.line(screen,BLACK,(cart.rect.right,pulley.top),(pulley.x,pulley.top),1)     #Connects string from cart to top pulley
    pygame.draw.arc(screen,BLACK,[pulley.left,pulley.top,2*pulley.radius,2*pulley.radius],0,math.pi/2,1)    #Wraps around pulley

    pygame.draw.line(screen,BLACK,(pulley.right,pulley.y),(massHolder.rect.centerx,massHolder.rect.top),1)  #Pulley to mass holder

    equipment.draw(screen)  # Draws Equipment
    pulley.draw()  # Draw Pulley
    massHolder.drawWeights()    #Draws Weights for massHolder
    cart.drawWeights()          #Draws Weights for Cart

    screen.blit(button,[100,300])


    if not isPaused:

        speed = massHolder.getSpeed()  # Fetches current speed

        if cart.rect.right + speed < pulley.left:  # If next shift is before pulley
            cart, massHolder = shift(cart, massHolder, speed)  # Move cart
        elif cart.rect.right == pulley.left:  # If cart is touching the pulley
            cart, massHolder = switchWeights(cart, massHolder)
            cart.rect.center = cart.startCenter
            massHolder.rect.center = massHolder.startCenter
        else:  # If the cart is about to hit the pulley
            cart.rect.right = pulley.left

    pygame.display.flip() #Updates screen

# Be IDLE friendly
pygame.quit()

