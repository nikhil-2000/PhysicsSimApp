from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

import pip

required_pkgs = ['pygame', 'matplotlib']
installed_pkgs = [pkg.key for pkg in pip.get_installed_distributions()]

for package in required_pkgs:
    if package not in installed_pkgs:
        with suppress_stdout():
            pip.main(['install', package])

# The previous lines were taken from https://stackoverflow.com/questions/10272879/how-do-i-import-a-python-script-from-a-sibling-directory
# It explained how to access modules in sibling directories

import pygame
import resources.resourceManager as resourceManager
import textwrap
import externalModules.pgu.pgu.gui as gui
import externalModules.pgu.pgu.html as html


class HelpDialog(gui.Dialog):
    def __init__(self):

        instructions = """<p>
         1. Look at the Instructions Dialog<br>
         2. Input your variables<br>
         3. Click start experiment to begin the animation<br>
         4. While the animation is running, you can pause it by using the pause button or toggle labels using the show labels button<br>
         5. Once all the values in the table have been filled in, try and plot the graph<br>
         6. After plotting the graph yourself, you can look at the graph that should have been plotted<br>
         7. Finally answer the question to see if you have understood the experiment correctly<br>
         </p>
         """
        #Adding the method to the document which html
        doc = html.HTML(instructions,width = 800)

        tbl = gui.Table()

        tbl.tr()
        tbl.td(gui.Image(resourceManager.exampleExperiment))
        tbl.tr()
        tbl.td(doc)
        #tbl.td(instructions)

        gui.Dialog.__init__(self,gui.Label("Help"), tbl)

def createButton(imgName, text):
    splitText = textwrap.wrap(text, width=30)  # Splits text and sets width of line to 30 characters

    #Loads Image
    img = pygame.image.load(imgName)
    #Stretches Image keeping height:width ratio constant
    height = int(250*img.get_height()/img.get_width())
    img = pygame.transform.scale(img,(250,height))

    #If the image is too tall
    if img.get_height() > 80:
        #Resize with max height
        height = 80
        width = int(height*img.get_width()/img.get_height())
        img = pygame.transform.scale(img,(width,height))

    #Add Image and label to table
    main = gui.Table()
    main.tr()
    main.td(gui.Image(img))
    for each in splitText:  # Puts each line in a label then adds it to the widget
        main.tr()
        main.td(gui.Label(each))

    return gui.Button(main, height=130, width=250)


def generateLayout(app):
    pygame.font.init()
    font = pygame.font.SysFont("cambria", 60)
    text = font.render("Main Menu", True, (0, 128, 0))

    menuTable = gui.Table(width=800, height=600)
	
    btnStyle = {"padding":10}
    def help_cb():
        dlg = HelpDialog()
        dlg.open()

    help = gui.Button("Help", height=50, width=100)
    help.connect(gui.CLICK,help_cb)

    menuTable.tr()
    menuTable.td(gui.Label(""))
    menuTable.td(gui.Image(text))
    menuTable.td(help)
    menuTable.tr()

    def btn1_cb():
        import Experiments.ResistivityOfAMetal.experiment as e
        e.run()

    btn1 = createButton(resourceManager.menuResistivity, "Determination of the Resistivity of a Metal")
    menuTable.td(btn1,style = btnStyle)
    btn1.connect(gui.CLICK, btn1_cb)

    def btn2_cb():
        import Experiments.InternalResistance.experiment as e
        e.run()

    btn2 = createButton(resourceManager.menuInternalResistance, "Determination of the Internal Resistance of a Cell")
    menuTable.td(btn2,style = btnStyle)
    btn2.connect(gui.CLICK, btn2_cb)

    def btn3_cb():
        import Experiments.EstimateAbsoluteZero.experiment as e
        e.run()

    btn3 = createButton(resourceManager.menuAbsoluteZero, "Estimation of Absolute Zero by Use of the Gas Laws")
    menuTable.td(btn3,style = btnStyle)
    btn3.connect(gui.CLICK,btn3_cb)

    menuTable.tr()

    def btn4_cb():
        import Experiments.Newtons2ndLaw.experiment as e
        e.run()

    btn4 = createButton(resourceManager.menuNewtons2ndLaw, "Investigation of Newton's 2nd Law")
    menuTable.td(btn4,style = btnStyle)
    btn4.connect(gui.CLICK,btn4_cb)


    def btn5_cb():
        import Experiments.RadioactiveDecay.experiment as e
        e.run()

    btn5 = createButton(resourceManager.menuRadioactiveDecay, "Investigation of Radioactive Decay")
    menuTable.td(btn5,style = btnStyle)
    btn5.connect(gui.CLICK,btn5_cb)

    def btn6_cb():
        import Experiments.Measureg.experiment as e
        e.run()

    btn6 = createButton(resourceManager.menugByFrefall, "Measurement of g by free-fall")
    menuTable.td(btn6,style = btnStyle)
    btn6.connect(gui.CLICK,btn6_cb)

    menuTable.tr()

    def btn7_cb():
        import Experiments.SHCofSolid.experiment as e
        e.run()

    btn7 = createButton(resourceManager.menuSHC, "Measurement of the Specific Heat Capacity for a Solid")
    menuTable.td(btn7,col= 1,style = btnStyle)
    btn7.connect(gui.CLICK,btn7_cb)

    return menuTable


def run():
    pygame.init()  # Intialise Pygame Module
    pygame.font.init()
    app = gui.Desktop(width=900, height=600)  # Sets the size and type of app
    app.connect(gui.QUIT, pygame.quit)  # Adds functionality to close button to quit app

    app.run(generateLayout(app))


if __name__ == '__main__':
    run()
