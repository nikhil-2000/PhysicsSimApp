import pygame
import random
pygame.init()

class s():
    def __init__(self,colour):
        self.rect = pygame.Rect(0,0,sWidth,sHeight)
        self.colour = colour
        self.spritesToDraw = pygame.sprite.Group()
        for i in range(10):
            x = random.randrange(0,sWidth - 100)
            y = random.randrange(0,sHeight - 100)
            p = testSprites(x,y)
            self.spritesToDraw.add(p)

    

class testSprites(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface([100,100])
        self.image.fill(PURPLE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        


BLACK   = (  0,  0,  0)
WHITE   = (255,255,255)
BLUE    = (  0,  0,255)
GREEN   = (  0, 255, 0)
RED     = (255,   0, 0)
PURPLE  = (255,  0,255)

sWidth,sHeight = 800,600


screen = pygame.display.set_mode([sWidth,sHeight])
s1 = s(RED)
s2 = s(BLUE)

c = s1

ret = pygame.Rect(0,0,sWidth,sHeight)
currentColor = RED


clock = pygame.time.Clock()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if c == s1:
                c = s2
            else:
                c = s1
        if event.type == pygame.QUIT:
                done = True

    screen.fill(WHITE)
    pygame.draw.rect(screen,c.colour,c.rect)
    c.spritesToDraw.draw(screen)
    pygame.display.flip()
    
    

    clock.tick(60)

pygame.quit()
    
