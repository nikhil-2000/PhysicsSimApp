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




def main():
    pygame.init()
    app = gui.Desktop(width = 800,height = 600)
    app.connect(gui.QUIT,app.quit,None)

    def createButton2(imgName,text,adj):
        firstpart, secondpart = text[:len(text)//2 +adj], text[len(text)//2 +adj:]
        main = gui.Table()
        main.tr()
        main.td(gui.Image(imgName))
        main.tr()
        main.td(gui.Label(firstpart))
        main.tr()
        main.td(gui.Label(secondpart))
        return gui.Button(main,height = 130,width = 200)


    font = pygame.font.SysFont("comicsansms", 60)
    text = font.render("Main Menu",True, (0, 128, 0))

    menuTable = gui.Table(width = 800,height = 600)

    RofMetalImg = pygame.image.load(resourceManager.resistivityOfAMetalDiagram)
    RofMetalImg = pygame.transform.scale(RofMetalImg,(256,200))
    IRImg = pygame.image.load(resourceManager.internalResistanceDiagram)
    IRImg = pygame.transform.scale(IRImg,(350,200))

    def cbFunc():
        app.quit()
        
        import Tests.TestExperimentPGU as exp1
        exp1.main()
    a = createButton2(resourceManager.atomImg,"Determination of the Resistivity of a Metal",0)
    a.connect(gui.CLICK,cbFunc)


    menuTable.tr()
    menuTable.td(gui.Label(""))
    menuTable.td(gui.Image(text))
    menuTable.td(gui.Button("Help",height = 50,width = 100))
    menuTable.tr()
    menuTable.td(a)
    menuTable.td(createButton2(resourceManager.atomImg,"Determination of the Internal Resistance of a Cell",4))
    menuTable.td(createButton2(resourceManager.atomImg,"Estimation of Absolute Zero by Use of the Gas Laws",6))
    menuTable.tr()
    menuTable.td(createButton2(resourceManager.atomImg,"Investigation of Newton’s Second Law",-1))
    menuTable.td(createButton2(resourceManager.atomImg,"Investigation of Radioactive Decay",0))
    menuTable.td(createButton2(resourceManager.atomImg,"Measurement of g by free-fall",0))
    menuTable.tr()
    menuTable.td(createButton2(resourceManager.atomImg,"Measurement of the Specific Heat Capacity for a Solid",1),col = 1)

    app.run(menuTable)

main()
