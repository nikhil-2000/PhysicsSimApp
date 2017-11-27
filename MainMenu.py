import os
import sys

sys.path.append(os.path.abspath('..'))

# The previous lines were taken from https://stackoverflow.com/questions/10272879/how-do-i-import-a-python-script-from-a-sibling-directory
# It explained how to access modules in sibling directories

import pygame
import resources.resourceManager as resourceManager
import textwrap
import externalModules.pgu.pgu.gui as gui


def createButton(imgName, text):
    splitText = textwrap.wrap(text, width=30)  # Splits text and sets width of line to 30 characters
    main = gui.Table()
    main.tr()
    main.td(gui.Image(imgName))
    for each in splitText:  # Puts each line in a label then adds it to the widget
        main.tr()
        main.td(gui.Label(each))

    return gui.Button(main, height=130, width=250)


def generateLayout(app):
    pygame.font.init()
    font = pygame.font.SysFont("trajan", 100)
    text = font.render("Menu", True, (0, 128, 0))

    menuTable = gui.Table(width=800, height=600)

    menuTable.tr()
    menuTable.td(gui.Label(""))
    menuTable.td(gui.Image(text))
    menuTable.td(gui.Button("Help", height=50, width=100))
    menuTable.tr()

    def btn1_cb():
        import Experiments.ResistivityOfAMetal.experiment as e
        e.run()

    btn1 = createButton(resourceManager.atomImg, "Determination of the Resistivity of a Metal")
    menuTable.td(btn1)
    btn1.connect(gui.CLICK, btn1_cb)

    def btn2_cb():
        import Experiments.InternalResistance.experiment as e
        e.run()

    btn2 = createButton(resourceManager.atomImg, "Determination of the Internal Resistance of a Cell")
    menuTable.td(btn2)
    btn2.connect(gui.CLICK, btn2_cb)

    def btn3_cb():
        import Experiments.EstimateAbsoluteZero.experiment as e
        e.run()

    btn3 = createButton(resourceManager.atomImg, "Estimation of Absolute Zero by Use of the Gas laws,")
    menuTable.td(btn3)
    btn3.connect(gui.CLICK,btn3_cb)

    menuTable.tr()

    def btn4_cb():
        import Experiments.Newtons2ndLaw.experiment as e
        e.run()

    btn4 = createButton(resourceManager.atomImg, "Investigation of Newton's 2nd Law")
    menuTable.td(btn4)
    btn4.connect(gui.CLICK,btn4_cb)


    def btn5_cb():
        import Experiments.RadioactiveDecay.experiment as e
        e.run()

    btn5 = createButton(resourceManager.atomImg, "Investigation of Radioactive Decay")
    menuTable.td(btn5)
    btn5.connect(gui.CLICK,btn5_cb)

    def btn6_cb():
        import Experiments.Measureg.experiment as e
        e.run()

    btn6 = createButton(resourceManager.atomImg, "Measurement of g by free-fall")
    menuTable.td(btn6)
    btn6.connect(gui.CLICK,btn6_cb)

    menuTable.tr()

    def btn7_cb():
        import Experiments.SHCofSolid.experiment as e
        e.run()

    btn7 = createButton(resourceManager.atomImg, "Measurement of the Specific Heat Capacity for a Solid")
    menuTable.td(btn7,col= 1)
    btn7.connect(gui.CLICK,btn7_cb)

    return menuTable


def run():
    pygame.init()  # Intialise Pygame Module
    pygame.font.init()
    app = gui.Desktop(width=900, height=600)  # Sets the size and type of app
    app.connect(gui.QUIT, pygame.quit, None)  # Adds functionality to close button to quit app

    app.run(generateLayout(app))


if __name__ == '__main__':
    run()
