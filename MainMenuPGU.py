import pygame
from pygame.locals import *
from pgu import gui
from Color import *

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

    RofMetalImg = pygame.image.load("ResistivityOfAMetal.jpg")
    RofMetalImg = pygame.transform.scale(RofMetalImg,(256,200))
    IRImg = pygame.image.load("InternalResistance.jpg")
    IRImg = pygame.transform.scale(IRImg,(350,200))

    def cbFunc():
        app.quit()
        import TestExperimentPGU as exp1
        exp1.main()
    a = createButton2("Ball1.png","Determination of the Resistivity of a Metal",0)
    a.connect(gui.CLICK,cbFunc)


    menuTable.tr()
    menuTable.td(gui.Label(""))
    menuTable.td(gui.Image(text))
    menuTable.td(gui.Button("Help",height = 50,width = 100))
    menuTable.tr()
    menuTable.td(a)
    menuTable.td(createButton2("Ball1.png","Determination of the Internal Resistance of a Cell",4))
    menuTable.td(createButton2("Ball1.png","Estimation of Absolute Zero by Use of the Gas Laws",6))
    menuTable.tr()
    menuTable.td(createButton2("Ball1.png","Investigation of Newton’s Second Law",-1))
    menuTable.td(createButton2("Ball1.png","Investigation of Radioactive Decay",0))
    menuTable.td(createButton2("Ball1.png","Measurement of g by free-fall",0))
    menuTable.tr()
    menuTable.td(createButton2("Ball1.png","Measurement of the Specific Heat Capacity for a Solid",1),col = 1)

    app.run(menuTable)

main()
