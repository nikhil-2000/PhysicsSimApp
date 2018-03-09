import pygame, sys
import resources.resourceManager as resM
pygame.init()

window = pygame.display.set_mode((200, 200))
background = pygame.Surface((window.get_size()))
background.fill((255, 255, 255))
image = pygame.image.load(resM.heatArrow)
image2 = pygame.image.load(resM.heatArrow)


image = image.convert()
rect = image.get_rect()

image2 = image2.convert_alpha()
rect2 = image2.get_rect()

rect2.left = rect.width + 1

i = 0
while True:
  for event in pygame.event.get():
    if event.type == 12:
      pygame.quit()
      sys.exit()

  image.set_alpha(i)
  image2.set_alpha(i)

  window.fill((255, 255, 255))
  window.blit(background, background.get_rect())
  window.blit(image, rect)
  window.blit(image2, rect2)

  if i == 255:
    i = 0
  else:
    i += 1

  pygame.display.update()
  pygame.time.Clock().tick(60)