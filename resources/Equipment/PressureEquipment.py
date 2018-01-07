import pygame
import resources.resourceManager as resM
import resources.Colour as colours
import math
import random
import externalModules.InAppPhysics.CircleCollisions2 as collisions


class Thermometer(pygame.sprite.Sprite):
    def __init__(self,x,y,height):
        self.minTemp = 10
        self.maxTemp = 100
        super(Thermometer, self).__init__()

        img = pygame.image.load(resM.thermometerImg)
        self.image = pygame.transform.scale(img,(int(height * (224/1018)),height))

        self.rect = self.image.get_rect()
        self.rect.center = x,y
        self.markerStart = self.rect.centerx - 11, self.rect.bottom - ((2 / 13.8) * self.rect.height)
        self.thermometerRed= (204,1,2)



    def setupMarker(self,screen,startTemp):
        startTemp = int(startTemp)
        self.drawMarker(screen,startTemp)

    def drawMarker(self,screen,temp):
        self.markerEnd = self.markerStart[0],self.markerStart[1] - self.getLength(temp)
        pygame.draw.line(screen, self.thermometerRed,self.markerStart,self.markerEnd,int(self.rect.width * (0.4/1.6)))

    def getLength(self,temp):
        return ((temp-self.minTemp)/(self.maxTemp - self.minTemp)) * (self.markerStart[1] -self.rect.top )


class PressureGauge(pygame.sprite.Sprite):
    def __init__(self,x,y,radius):
        super(PressureGauge, self).__init__()
        self.min = 90
        self.max = 130

        img = pygame.image.load(resM.pressureGaugeImg)
        self.image = pygame.transform.scale(img,(2*radius,2*radius))
        self.radius = radius - 5

        self.rect = self.image.get_rect()
        self.rect.center = x,y
        self.startAngle = math.pi/4

    def setupPointer(self,startPressure,screen):
        self.drawPointer(screen,startPressure)

    def getPoints(self,pressure):
        additionalAngle = (1.5*math.pi) * (pressure - self.min)/(self.max - self.min)
        angle = self.startAngle + additionalAngle
        xLen = self.radius * math.sin(angle)
        yLen = self.radius * math.cos(angle)
        return self.rect.centerx - xLen, self.rect.centery + yLen


    def drawPointer(self,screen,pressure):
        self.endPoint = self.getPoints(pressure)
        pygame.draw.line(screen,colours.RED,self.rect.center,self.endPoint,2)


class WaterBeaker(pygame.sprite.Sprite):
    def __init__(self,x,y,height):
        super(WaterBeaker, self).__init__()

        img = pygame.image.load(resM.absoluteZeroDiagramImg)
        height = height - 20
        width = int((300/242) * height)
        self.image = pygame.transform.scale(img,(width,height))
        self.rect = self.image.get_rect()

        self.rect.center = x,y

class Atom():
    def __init__(self,diameter,minTemp,maxTemp):

        self.x = random.randrange(260,300)
        self.y = random.randrange(250,290)
        self.minSpeed = 1
        self.maxSpeed = 10
        self.angle = math.radians(random.randrange(0,360))

        self.minTemp = minTemp
        self.maxTemp = maxTemp

        self.startspeedx = self.minSpeed * math.cos(self.angle)
        self.startspeedy = self.minSpeed * math.sin(self.angle)

        self.speedx = self.startspeedx
        self.speedy = self.startspeedy

        self.radius = diameter/2

    def move(self):
        self.x += self.speedx
        self.y += self.speedy

    def updateSpeed(self,currentTemp):
        #speedDiff = minSpeed + (speedRange * fractionOfTempRange)

        self.speedx = self.startspeedx * (1+ (currentTemp - self.minTemp)/(self.maxTemp - self.minTemp))
        self.speedy = self.startspeedy * (1+ (currentTemp - self.minTemp)/(self.maxTemp - self.minTemp))

        if self.speedx > self.maxSpeed or self.speedy > self.maxSpeed:
            self.speedx = 5 * math.cos(math.atan(self.speedx/self.speedy))
            self.speedy = 5 * math.sin(math.atan(self.speedx/self.speedy))

    def turnAround(self):
        self.speedx *= -1
        self.speedy *= -1

        self.startspeedx *= -1
        self.startspeedy *= -1

    def setStartSpeeds(self):
        if (self.speedx < 0 and self.startspeedx > 0) or (self.speedx > 0 and self.startspeedx < 0):
            self.startspeedx = -self.startspeedx

        if (self.speedy < 0 and self.startspeedy > 0) or (self.speedy > 0 and self.startspeedy < 0):
            self.startspeedy = -self.startspeedy


    def draw(self,screen):
        pygame.draw.circle(screen,colours.RED,(int(self.x),int(self.y)),int(self.radius))



class BulbBeaker():
    def __init__(self,minTemp,maxTemp):

        self.minTemp = minTemp
        self.maxTemp = maxTemp
        self.radius = 73
        self.origin = 283,271   # The beaker center
        self.atoms = []
        for i in range(20):     # Generating the atoms
            self.atoms.append(Atom(10,minTemp,maxTemp))

        self.rect = pygame.Rect((0,0),(self.radius * 2, self.radius * 2))
        self.rect.center = self.origin

    def moveAtoms(self,currentTemp):
        for atom in self.atoms:
            atom.updateSpeed(currentTemp)
            atom.move()

        for atom in self.atoms: #This loop checks if it hits the sides
            #Calculating Distances
            xDistanceFromOrigin = atom.x - self.origin[0]
            yDistanceFromOrigin = atom.y - self.origin[1]

            distance = math.hypot(xDistanceFromOrigin,yDistanceFromOrigin)
            if distance >= self.radius-atom.radius:# Checks if atom is further than radious
                #Turns the atom around
                atom.turnAround()
                #atom.x,atom.y = self.origin

        for atom in self.atoms: #Checks if atoms collide with each other
            for atom2 in self.atoms:
                if atom != atom2:
                    centresDistance = math.hypot(atom.x - atom2.x , atom.y - atom2.y)
                    if centresDistance <= ( atom.radius * 2):
                        atom = collisions.CircleCollide(atom,atom2)

    def drawAtoms(self,screen):
        for atom in self.atoms:
            atom.draw(screen)



