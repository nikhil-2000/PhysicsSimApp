import pygame
import resources.resourceManager as resM
import resources.Colour as colour

class Voltmeter(pygame.sprite.Sprite):
    def __init__(self,x,y,radius):
        super(Voltmeter, self).__init__()

        self.image = pygame.image.load(resM.voltmeterImg)
        self.image = pygame.transform.scale(self.image,(radius,radius))


        self.rect = self.image.get_rect()
        self.rect.center = x,y
        self.centerX = self.rect.center[0]
        self.centerY = self.rect.center[1]



class Ammeter(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super(Ammeter, self).__init__()

        self.image = pygame.image.load(resM.ammeterImg)
        self.image = pygame.transform.scale(self.image, (radius, radius))

        self.rect = self.image.get_rect()
        self.rect.center = x,y
        self.centerX = self.rect.center[0]
        self.centerY = self.rect.center[1]



class Battery(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super(Battery, self).__init__()

        self.image = pygame.image.load(resM.batteryImg)
        self.image = pygame.transform.rotate(self.image,90)
        self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()
        self.rect.center = x,y
        self.centerX = self.rect.center[0]
        self.centerY = self.rect.center[1]

class ConstantanWire(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        super(ConstantanWire, self).__init__()
        self.image = pygame.Surface((width,height))
        self.image.fill(colour.SILVER)
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        self.centerX = self.rect.center[0]
        self.centerY = self.rect.center[1]


class Resistor(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        super(Resistor, self).__init__()


        self.rect = pygame.Rect(x,y,width,height)
        self.rect.center = x,y
        self.centerX = self.rect.center[0]
        self.centerY = self.rect.center[1]

    def draw(self,screen):
        pygame.draw.rect(screen,colour.BLACK,self.rect,1)


