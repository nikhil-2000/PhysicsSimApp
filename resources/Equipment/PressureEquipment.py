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
    def __init__(self,diameter):

        self.x = random.randrange(260,300)
        self.y = random.randrange(250,290)
        self.minSpeed = 1
        self.maxSpeed = 5
        self.angle = math.radians(random.randrange(0,360))

        temp = 20
        minTemp = 10
        maxTemp = 100
        self.speed = self.minSpeed +  (self.maxSpeed - self.minSpeed)*(temp - minTemp)/(maxTemp - minTemp)

        self.speedx = self.speed * math.cos(self.angle)
        self.speedy = self.speed * math.sin(self.angle)

        self.radius = diameter/2




    def move(self):
        self.x += self.speedx
        self.y += self.speedy

    def getComponents(self):
        return self.speed * math.cos(self.angle), self.speed * math.sin(self.angle)

    def updateSpeed(self,temp,maxTemp,minTemp):
        self.speed += 0.1
        self.speedx = self.speed * math.cos(self.angle)
        self.speedy = self.speed * math.sin(self.angle)



    def draw(self,screen):
        pygame.draw.circle(screen,colours.RED,(int(self.x),int(self.y)),int(self.radius))



class BulbBeaker():
    def __init__(self):

        self.radius = 74
        self.origin = 283,271
        self.atoms = []
        for i in range(30):
            self.atoms.append(Atom(7))

    def moveAtoms(self):
        for atom in self.atoms:
            atom.move()

        for atom in self.atoms:
            xDistanceFromOrigin = atom.x - self.origin[0]
            yDistanceFromOrigin = atom.y - self.origin[1]
            if xDistanceFromOrigin < 0:
                xDistanceFromOrigin *= -1

            if yDistanceFromOrigin < 0:
                yDistanceFromOrigin *= -1

            xDistanceFromOrigin += atom.radius
            yDistanceFromOrigin += atom.radius

            distance = math.hypot(xDistanceFromOrigin,yDistanceFromOrigin)
            if distance >= self.radius:

                atom.speedx *= -1
                atom.speedy *= -1

                atom.x += atom.speedx
                atom.y += atom.speedy
                #atom.rect.center = self.origin

        for atom in self.atoms:
            for atom2 in self.atoms:
                if atom != atom2:
                    centresDistance = math.hypot(atom.x - atom2.x , atom.y - atom2.y)
                    #print("CentreDistance:", centresDistance , "Diameters",atom.diameter)
                    if centresDistance <= ( atom.radius * 2):
                        collisions.CircleCollide(atom,atom2)


    def drawAtoms(self,screen):
        for atom in self.atoms:
            atom.draw(screen)

    def updateSpeeds(self,currentTemp,minTemp,maxTemp):
        for atom in self.atoms:
            atom.updateSpeed(currentTemp,maxTemp,minTemp)



