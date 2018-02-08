import pygame
from resources.Colour import *
import random
import externalModules.InAppPhysics.CircleCollisions2 as collisions
import math


class Container:
    def __init__(self,x,y,width,height):
        #Rectangle represents the walls of the container
        self.rect = pygame.Rect(x,y,width,height)
        #Represents the last decayed atom in the list of atoms
        self.lastDecayedIndex = -1

        #Creates atoms
        self.atoms = []
        for i in range(200):
            self.atoms.append(Atom(self.rect,3))

        #The number of atoms which are undecayed
        self.actualUndecayed = len(self.atoms)


    def draw(self,screen):
        #Moves all atoms then draws them and the container onto the screen
        self.moveAtoms()

        pygame.draw.rect(screen,WHITE,self.rect,2)
        for atom in self.atoms:
            atom.draw(screen)


    def moveAtoms(self):
        
        for atom in self.atoms:#For all atoms
            atom.move()
            #Checks if it hit a container wall
            self.checkCollision(atom)

            #Checks if atoms hit each other
            for atom2 in self.atoms:
                if atom != atom2:
                    centresDistance = math.hypot(atom.x - atom2.x, atom.y - atom2.y)
                    if centresDistance <= (atom.radius * 2):
                        atom = collisions.CircleCollide(atom, atom2)
                        atom.x = atom.x
                        atom.y = atom.y

    def checkCollision(self,atom):
        #Check wall collision
        if atom.x + atom.radius >= self.rect.right or atom.x - atom.radius <= self.rect.left:
            atom.speedx *=-1
            atom.x += atom.speedx

        if atom.y - atom.radius <= self.rect.top or atom.y + atom.radius >= self.rect.bottom:
            atom.speedy *= -1
            atom.y += atom.speedy

    def decayAtoms(self,calculatedDecay):
        #Calculates how many atoms should be decayed
        atomsToDecay = self.actualUndecayed - calculatedDecay

        #Decays the correct amount of atoms while updating variables
        for i in range(atomsToDecay):
            self.lastDecayedIndex += 1
            self.actualUndecayed -= 1
            self.atoms[self.lastDecayedIndex].decay()   #Changes colour of atom

class Atom:
    def __init__(self,rect,radius):
        #Puts the atom in a random area of the container
        self.x = random.randint(rect.left+radius+10,rect.right-radius-10)
        self.y = random.randint(rect.top+radius+10,rect.bottom-radius-10)

        self.decayed = False
        self.radius = radius

        #Generates the components of velocity randomly
        self.speedx = random.randint(-20,20)/10
        self.speedy = random.randint(-20,20)/10
        
    def move(self):
        #Moves the atom by its speed in both directions
        self.x = self.x + self.speedx
        self.y = self.y + self.speedy


    def draw(self,screen):
        #Decides colour depending on decay status
        if self.decayed:
            col = BLUE
        else:
            col = RED

        #Coordinates have to be rounded before plotting
        x = int(self.x)
        y = int(self.y)

        #Draws the atom
        pygame.draw.circle(screen,col,(x,y),self.radius)

    def setStartSpeeds(self):
        #Function requires for collision module
        #Only here to stop the program crashing
        pass

    def decay(self):
        #Decays the atom
        self.decayed = True