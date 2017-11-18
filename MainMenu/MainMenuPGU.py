import os
import sys
sys.path.append(os.path.abspath('..'))

#The previous lines were taken from https://stackoverflow.com/questions/10272879/how-do-i-import-a-python-script-from-a-sibling-directory
#It explained how to access modules in sibling directories

import pygame
from pygame.locals import *
from externalModules.pgu.pgu import gui
from resources import Colour
import resources.resourceManager as resourceManager
import textwrap



def createButton(imgName, text):
    ##firstpart, secondpart = text[:len(text) // 2 + adj], text[len(text) // 2 + adj:]
    splitText = textwrap.wrap(text,width = 30) # Splits text and sets width of line to 30 characters
    main = gui.Table()
    main.tr()
    main.td(gui.Image(imgName))
    for each in splitText: # Puts each line in a label then adds it to the widget
        main.tr()
        main.td(gui.Label(each))

    return gui.Button(main, height=130, width=300)

def generateLayout(app):
    font = pygame.font.SysFont("comicsansms", 60)
    text = font.render("Main Menu", True, (0, 128, 0))

    menuTable = gui.Table(width = 1000,height = 600)

    menuTable.tr()
    menuTable.td(gui.Label(""))
    menuTable.td(gui.Image(text))
    menuTable.td(gui.Button("Help",height = 50,width = 100))
    menuTable.tr()

    btn1 = createButton(resourceManager.atomImg,"Determination of the Resistivity of a Metal")
    menuTable.td(btn1)

    menuTable.td(createButton(resourceManager.atomImg,"Determination of the Internal Resistance of a Cell"))
    menuTable.td(createButton(resourceManager.atomImg,"Estimation of Absolute Zero by Use of the Gas Laws"))
    menuTable.tr()
    menuTable.td(createButton(resourceManager.atomImg,"Investigation of Newton’s Second Law"))
    menuTable.td(createButton(resourceManager.atomImg,"Investigation of Radioactive Decay"))
    menuTable.td(createButton(resourceManager.atomImg,"Measurement of g by free-fall"))
    menuTable.tr()
    menuTable.td(createButton(resourceManager.atomImg,"Measurement of the Specific Heat Capacity for a Solid"),col = 1)
    return menuTable




def main():
    pygame.init()# Intialise Pygame Module
    app = gui.Desktop(width = 1000,height = 600)#Sets the size and type of app
    app.connect(gui.QUIT,app.quit,None) # Adds functionality to close button to quit app

    app.run(generateLayout(app))

main()
