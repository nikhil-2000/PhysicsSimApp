import resources.Colour as cols
import pygame
import math
import resources.resourceManager as resM


class Cart(pygame.sprite.Sprite):
    def __init__(self,screen,bench):
        #Setting Attributes
        super(Cart, self).__init__()
        self.screen = screen
        img = pygame.image.load(resM.cartImg)
        self.image = pygame.transform.scale(img,(150,170))

        self.bench = bench                          #Needs Bench as reference point

        self.rect = self.image.get_rect()
        self.rect.left = self.bench.rect.left + 20  #Places cart relative to bench
        self.rect.bottom = self.bench.rect.top

        self.startCenter = self.rect.center         #Taken now to cart back to start Point

        self.noOfWeights = 0                        #Will determine speed

    def drawWeights(self):
        yCoord = self.rect.bottom - 65              #Marks start point of mass holder on cart
        for i in range(self.noOfWeights):
            weight = pygame.Surface((40, 10))       #The yellow part of the weight
            weight.fill(cols.YELLOW)
            rect = weight.get_rect()                #Black outline of Weight
            rect.center = self.rect.centerx,yCoord
            self.screen.blit(weight,rect)           #Draw the Yellow surface
            pygame.draw.rect(self.screen,cols.BLACK,rect,1)  #Draw Black Outline
            yCoord -= 10                            #Increment Y coord by weight height

class Bench(pygame.sprite.Sprite):
    def __init__(self,screen,y):
        #This Object is the table and fairly simple, it doesn't require any other methods
        #This acts as a reference point for:
            # The cart
            # The Pulley
            # The Dataloggers
        super(Bench, self).__init__()
        self.screen = screen
        self.image = pygame.Surface([450,70])
        self.image.fill(cols.BROWN)

        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.bottom = y

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
        pygame.draw.circle(self.screen,cols.RED,(self.x,self.y),self.radius)

class MassHolder(pygame.sprite.Sprite):
    def __init__(self,screen,pulley):
        super(MassHolder, self).__init__()

        #This will have the masses which the cart doesn't have
        #Determines the speed of the cart
        img = pygame.image.load(resM.massHolderImg)
        self.image = pygame.transform.scale(img,(50,175))
        self.screen = screen

        self.pulley = pulley

        self.rect = self.image.get_rect()
        self.rect.centerx = self.pulley.x + self.pulley.radius
        self.rect.top = self.pulley.bench.rect.bottom - 30

        self.noOfWeights = 0
        self.startCenter = self.rect.center
        self.time = 0


    def drawWeights(self):#Draws weights in a similair style to the cart
        yCoord = self.rect.bottom - 15
        for i in range(self.noOfWeights):
            weight = pygame.Surface((40, 10))
            weight.fill(cols.YELLOW)
            rect = weight.get_rect()
            rect.center = self.rect.centerx,yCoord
            self.screen.blit(weight,rect)
            pygame.draw.rect(self.screen,cols.BLACK,rect,1)
            yCoord -= 10

    def getSpeed(self,weightOnMassHolder,totalMass):
        #This will accelerate the cart
        self.time += 1/60
        self.acceleration = weightOnMassHolder/(totalMass)
        return  self.acceleration* self.time


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
