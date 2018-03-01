import pygame
import resources.resourceManager as resM


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
        self.thermometer.rect.bottom = self.x + self.thermometerHeight
        print(self.thermometer.rect.bottom)
        self.thermometer.markerStart = self.thermometer.rect.centerx,self.thermometer.rect.bottom - 40

    def insertHeater(self):
        self.heater = Heater()
        self.heater.rect = self.heater.image.get_rect()
        self.heater.rect.left = self.heaterBasePoint - self.heaterWidth - 3
        self.heater.rect.bottom = self.x + self.heaterHeight

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
