import pygame
import resources.resourceManager as resM
import resources.Colour as colours
import math



class Thermometer(pygame.sprite.Sprite):
    def __init__(self,x,y,height):
        self.minTemp = 10
        self.maxTemp = 100
        super(Thermometer, self).__init__()

        img = pygame.image.load(resM.thermometerImg)
        self.image = pygame.transform.scale(img,(int(height * (224/1018)),height))

        self.rect = self.image.get_rect()
        self.rect.center = x,y
        self.markerStart = self.rect.centerx, self.rect.bottom - ((2 / 13.8) * self.rect.height)
        self.thermometerRed= (204,1,2)


    def setupMarker(self,screen,startTemp):
        startTemp = int(startTemp)
        self.drawMarker(screen,startTemp)

    def drawMarker(self,screen,temp):
        self.markerEnd = self.markerStart[0],self.markerStart[1] + self.getLength(temp)
        pygame.draw.line(screen, self.thermometerRed,self.markerStart,self.markerEnd,int(self.rect.width * (0.4/5.2)))

    def getLength(self,temp):
        return (temp/(self.maxTemp - self.minTemp)) * (self.rect.top - self.markerStart[1])


class PressureGauge(pygame.sprite.Sprite):
    def __init__(self,x,y,radius):
        super(PressureGauge, self).__init__()
        self.min = 85
        self.max = 105

        img = pygame.image.load(resM.pressureGaugeImg)
        self.image = pygame.transform.scale(img,(2*radius,2*radius))
        self.radius = radius - 5

        self.rect = self.image.get_rect()
        self.rect.center = x,y

    def setupPointer(self,startPressure):
        pass

    def getPoints(self,pressure):
        angle = 2 * math.pi * (pressure - self.min)/(self.max - self.min)
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


