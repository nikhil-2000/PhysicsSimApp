import pygame
from resources.Colour import *
import random
import externalModules.InAppPhysics.CircleCollisions2 as collisions
import math


class Container:
    def __init__(self,x,y,width,height):
        self.rect = pygame.Rect(x,y,width,height)
        self.lastDecayedIndex = -1
        self.atoms = []
        for i in range(200):
            self.atoms.append(Atom(self.rect,3))

        self.actualUndecayed = len(self.atoms)


    def draw(self,screen):
        self.moveAtoms()

        pygame.draw.rect(screen,WHITE,self.rect,2)
        for atom in self.atoms:
            atom.draw(screen)


    def moveAtoms(self):
        
        for atom in self.atoms:
            atom.move()
            self.checkCollision(atom)
            for atom2 in self.atoms:
                if atom != atom2:
                    centresDistance = math.hypot(atom.x - atom2.x, atom.y - atom2.y)
                    if centresDistance <= (atom.radius * 2):
                        atom = collisions.CircleCollide(atom, atom2)
                        atom.x = atom.x
                        atom.y = atom.y

    def checkCollision(self,atom):
        if atom.x + atom.radius >= self.rect.right or atom.x - atom.radius <= self.rect.left:
            atom.speedx *=-1
            atom.x += atom.speedx

        if atom.y - atom.radius <= self.rect.top or atom.y + atom.radius >= self.rect.bottom:
            atom.speedy *= -1
            atom.y += atom.speedy

    def decayAtoms(self,atomsToDecay):

        for i in range(atomsToDecay):
            self.lastDecayedIndex += 1
            self.atoms[self.lastDecayedIndex].decay()

class Atom:
    def __init__(self,rect,radius):
        self.x = random.randint(rect.left+radius+10,rect.right-radius-10)
        self.y = random.randint(rect.top+radius+10,rect.bottom-radius-10)

        self.decayed = False
        self.radius = radius
        
        self.speedx = random.randrange(-20,20)/10
        self.speedy = random.randrange(-20,20)/10
        
    def move(self):
        self.x = self.x + self.speedx
        self.y = self.y + self.speedy


    def draw(self,screen):
        if self.decayed:
            col = BLUE
        else:
            col = RED

        x = int(self.x)
        y = int(self.y)

        pygame.draw.circle(screen,col,(x,y),self.radius)

    def setStartSpeeds(self):
        pass

    def decay(self):
        self.decayed = True