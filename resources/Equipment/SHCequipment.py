import pygame
import resources.resourceManager as resM
import math

class CopperBlock():
    def __init__(self, x, y, width, height):
        self.colour = (152, 153, 155)
        self.targetColour = (190, 70, 70)

        self.thermometer = None
        self.heater = None

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.thermometerBasePoint = x + width // 3
        self.heaterBasePoint = x + 2 * width // 3

        self.thermometerWidth = 20
        self.thermometerHeight = 200
        self.heaterWidth = 12
        self.heaterHeight = 120

        self.points = []
        self.points.append((x, y))
        self.points.append((self.thermometerBasePoint - self.thermometerWidth, y))
        self.points.append((self.thermometerBasePoint - self.thermometerWidth, y + self.thermometerHeight))
        self.points.append((self.thermometerBasePoint + self.thermometerWidth, y + self.thermometerHeight))
        self.points.append((self.thermometerBasePoint + self.thermometerWidth, y))
        self.points.append((self.heaterBasePoint - self.heaterWidth, y))
        self.points.append((self.heaterBasePoint - self.heaterWidth, y + self.heaterHeight))
        self.points.append((self.heaterBasePoint + self.heaterWidth, y + self.heaterHeight))
        self.points.append((self.heaterBasePoint + self.heaterWidth, y))
        self.points.append((x + width, y))
        self.points.append((x + width, y + height))
        self.points.append((x, y + height))

    def insertThermometer(self):
        self.thermometer = Thermometer()
        self.thermometer.image = pygame.transform.scale(self.thermometer.image,
                                                        (2 * self.thermometerWidth, self.thermometerHeight + 70))
        self.thermometer.rect = self.thermometer.image.get_rect()
        self.thermometer.rect.left = self.thermometerBasePoint - self.thermometerWidth
        self.thermometer.rect.bottom = self.y + self.thermometerHeight
        self.thermometer.markerStart = self.thermometer.rect.centerx,self.thermometer.rect.bottom - 40

    def insertHeater(self):
        self.heater = Heater()
        self.heater.image = pygame.transform.scale(self.heater.image,(2*self.heaterWidth + 15, self.heaterHeight + 30))
        self.heater.rect = self.heater.image.get_rect()
        self.heater.rect.left = self.heaterBasePoint - self.heaterWidth - 6
        self.heater.rect.bottom = self.y + self.heaterHeight

    def draw(self, screen):
        pygame.draw.polygon(screen, self.colour, self.points, 0)


class Thermometer(pygame.sprite.Sprite):
    def __init__(self):
        self.minTemp = 10
        self.maxTemp = 80
        super(Thermometer, self).__init__()

        img = pygame.image.load(resM.SHCThermometer)
        self.image = img

        self.rect = self.image.get_rect()
        self.markerStart = self.rect.centerx-3,self.rect.bottom - 20
        self.thermometerRed = (204, 0, 1)

    def setupMarker(self, screen, startTemp):
        startTemp = int(startTemp)
        self.drawMarker(screen, startTemp)

    def drawMarker(self, screen, temp):
        self.markerEnd = self.markerStart[0], self.markerStart[1] - self.getLength(temp)
        # print("Start",self.markerStart)
        # print("End",self.markerEnd)
        pygame.draw.line(screen, self.thermometerRed, self.markerStart, self.markerEnd,15)

    def getLength(self, temp):
        return ((temp - self.minTemp) / (self.maxTemp - self.minTemp)) * (self.markerStart[1] - self.rect.top - 11)

    def moveThermometerFromBottom(self, x, y):
        self.rect.bottom = y
        self.rect.centerx = x


class Heater(pygame.sprite.Sprite):
    def __init__(self):
        super(Heater, self).__init__()

        img = pygame.image.load(resM.SHCHeater)
        self.image = img

        self.rect = self.image.get_rect()

class HeatArrow(pygame.sprite.Sprite):
    def __init__(self,x,y,angle,factor):
        super(HeatArrow, self).__init__()
        img = pygame.image.load(resM.heatArrow)
        w = int(19 * factor)
        h = int(6 * factor)
        img = pygame.transform.scale(img,(w,h))
        img = pygame.transform.rotate(img,angle)
        self.image = pygame.Surface.convert(img)
        self.image.set_colorkey((255,255,255))

        self.rect = self.image.get_rect()
        self.rect.center = x,y
        self.startPos = x,y

        self.alpha = 255
        self.speed = 1.01
        self.angle = angle


    def fade(self):
        #self.image.set_colorkey((255,255,255))
        self.alpha -= 5
        if self.alpha <= 0:
            self.alpha = 255
            self.rect.center = self.startPos

        self.image.set_alpha(self.alpha)
        self.rect.x -= round(self.speed * math.cos(math.radians(self.angle)))
        self.rect.y += round(self.speed * math.sin(math.radians(self.angle)))


# def increaseRed(self):
#     if self.colour != self.targetColour:
#         if self.colour[0] < self.targetColour[0]: r = self.colour[0] + 1
#         elif self.colour[0] > self.targetColour[0]: r = self.colour[0] - 1
#         else: r= self.colour[0]
#
#         if self.colour[1] < self.targetColour[1]: g = self.colour[1] + 1
#         if self.colour[1] > self.targetColour[1]: g = self.colour[1] - 1
#         else: g= self.colour[1]
#
#
#         if self.colour[2] < self.targetColour[2]: b = self.colour[2] + 1
#         if self.colour[2] > self.targetColour[2]: b = self.colour[2] - 1
#         else: b= self.colour[2]
#
#         self.colour = (r,g,b)
