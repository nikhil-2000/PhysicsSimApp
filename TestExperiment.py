import pygame
# This is a comment to test bitbucket and git workflow
BLACK   = (  0,  0,  0)
WHITE   = (255,255,255)
BLUE    = (  0,  0,255)
GREEN   = (  0, 255, 0)
RED     = (255,   0, 0)
PURPLE  = (255,  0,255)

sWidth,sHeight = 800,600

pygame.init()

screen = pygame.display.set_mode([sWidth,sHeight])

clock = pygame.time.Clock()
done = False


class Experiment(object):
    def __init__(self,equipment):
        self.drawEquipment = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        for i in equipment:
            self.drawEquipment.add(i)

##    def checkCollision(self):
    
            
            

class Equipment(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ball1.png")
        self.image = pygame.transform.scale(self.image,(20,20))

        self.rect = self.image.get_rect()
        self.rect.x = sWidth/2
        self.rect.y = sHeight/2
        self.xSpeed = 5
        self.ySpeed = 5


beakerImg = pygame.image.load("beaker.png")
newDim = beakerImg.get_rect().width*3,beakerImg.get_rect().height*3
beakerImg = pygame.transform.scale(beakerImg,(newDim))
beaker = Equipment(beakerImg,(sWidth-newDim[0])/2 ,(sHeight-newDim[1])/2)
exp = Experiment([beaker])

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                exp.particles.add(Ball())

    for i in exp.particles:
        i.rect.x += i.xSpeed
        i.rect.y += i.ySpeed
    
    screen.fill(WHITE)
    exp.drawEquipment.draw(screen)
    exp.particles.draw(screen)

    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
    

            
