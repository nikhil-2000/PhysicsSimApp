
import pygame
import time
import random

pygame.font.init()


class Button(pygame.sprite.Sprite):
    def __init__(self,x,y,image,text):
        super().__init__()
        
        self.image = pygame.image.load(image)

        self.rect = self.image.get_rect()
        self.background = pygame.Rect(x-10,y-10,self.rect.width + 20, self.rect.height + 40)
        self.rect.x = x
        self.rect.y = y
        font = pygame.font.SysFont("comicsansms", 20)
        self.text = font.render(text,True,(RED))
        
        
        
pygame.init()
 
sWidth,sHeight = 800,600
 
from Color import *


screen = pygame.display.set_mode([sWidth,sHeight])
pygame.display.set_caption('Main Menu')
clock = pygame.time.Clock()

button = Button(100,100,"ball1.png","Exp1")
 
inMenu = True
while inMenu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inMenu = False

    screen.fill(BLUE)
    pygame.draw.rect(screen,GREEN,button.background)
    screen.blit(button.image,(button.rect.x,button.rect.y))
    screen.blit(button.text,(button.rect.x+(button.rect.width/2) - button.text.get_rect().width/2,button.rect.y + button.rect.height))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
