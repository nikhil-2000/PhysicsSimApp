import os
import sys
sys.path.append(os.path.abspath('..'))

import Experiments.creatingGraphs as graph
import Validation.validation as validation

#The previous lines were taken from https://stackoverflow.com/questions/10272879/how-do-i-import-a-python-script-from-a-sibling-directory
#It explained how to access modules in sibling directories

import pygame
from externalModules.pgu.pgu import gui, timer

class ErrorDlg(gui.Dialog):
    def __init__(self,msg):
        gui.Dialog.__init__(self,gui.Label("ERROR"),gui.Label(msg))

class VariablesDialog(gui.Dialog):
    def __init__(self,defaultVals,minRange,maxRange):
        explainLbl = gui.Label("Input your variables below")
        nOfResultsLbl = gui.Label("Have between 5-10 recordings")
        rangeStr = str("The range is " + str(minRange) + " to " + str(maxRange))
        rangeLbl = gui.Label(rangeStr)

        minIVUserLbl = gui.Label("Min")
        maxIVUserLbl = gui.Label("Max")
        intervalUserLbl = gui.Label("Interval")

        minIVUserInput = gui.Input()
        maxIVUserInput = gui.Input()
        intervalIVUserInput = gui.Input()

        minIVUnitLbl = gui.Label("cm")
        maxIVUnitLbl = gui.Label("cm")
        intervalIVUnitLbl = gui.Label("cm")

        buttonHeight = 50
        buttonWidth = 120

        okBtn = gui.Button("Enter",height=buttonHeight, width=buttonWidth)
        defaultBtn = gui.Button("Default Values",height=buttonHeight, width=buttonWidth)

        def okBtn_cb():
            minIV = minIVUserInput
            maxIV = maxIVUserInput
            interval = intervalIVUserInput

            isValidated,error = validation.validateInputs(minIV,maxIV,interval,maxRange,minRange)


        textTbl = gui.Table()
        inputTbl = gui.Table()
        buttonTbl = gui.Table()

        textTbl.tr()
        textTbl.td(explainLbl)
        textTbl.tr()
        textTbl.td(nOfResultsLbl)
        textTbl.tr()
        textTbl.td(rangeLbl)

        inputTblStyle = {'padding':10}
        inputTbl.tr()
        inputTbl.td(minIVUserLbl,style=inputTblStyle)
        inputTbl.td(minIVUserInput,style=inputTblStyle)
        inputTbl.td(minIVUnitLbl,style=inputTblStyle)
        inputTbl.tr()
        inputTbl.td(maxIVUserLbl,style=inputTblStyle)
        inputTbl.td(maxIVUserInput,style=inputTblStyle)
        inputTbl.td(maxIVUnitLbl,style=inputTblStyle)
        inputTbl.tr()
        inputTbl.td(intervalUserLbl,style=inputTblStyle)
        inputTbl.td(intervalIVUserInput,style=inputTblStyle)
        inputTbl.td(intervalIVUnitLbl,style=inputTblStyle)

        buttonTbl.tr()
        buttonTbl.td(okBtn,style=inputTblStyle)
        buttonTbl.td(defaultBtn,style=inputTblStyle)

        tbl = gui.Table()
        tbl.tr()
        tbl.td(textTbl)
        tbl.tr()
        tbl.td(inputTbl)
        tbl.tr()
        tbl.td(buttonTbl)

        gui.Dialog.__init__(self,gui.Label("Variables"),tbl)

class DrawingArea(gui.Widget):  # Same object as found in gui18.py in the pgu examples
    def __init__(self, width, height):
        gui.Widget.__init__(self, width=width, height=height)
        self.imageBuffer = pygame.Surface((width, height))

    def paint(self, surf):
        # Paint whatever has been captured in the buffer
        surf.blit(self.imageBuffer, (0, 0))

    # Call self function to take a snapshot of whatever has been rendered
    # onto the display over self widget.
    def save_background(self):
        disp = pygame.display.get_surface()
        self.imageBuffer.blit(disp, self.get_abs_rect())


class TableAreaTemplate(gui.Table):
    def __init__(self, width, height, app):
        gui.Table.__init__(self, width=width, height=height)
        self.app = app

    def setup(self):
        pass


# This will be run once the user has entered a valid set of variables

class MenuAreaTemplate(gui.Table):
    def __init__(self, width, height, app):
        gui.Table.__init__(self, width=width, height=height)
        self.app = app

    def setup(self):
        # All the buttons are created and organised here

        #The button variables are all created here
        self.graphBtn = createButton("Graph")

        self.variablesBtn = createButton("Input Variables")

        self.startExperimentBtn = createButton("Start Experiment")

        self.pauseExperimentBtn = createButton("Pause Experiment")

        self.restartExperimentBtn = createButton("Restart Experiment")

        self.instructionBtn = createButton("Instructions/Links")

        self.constantsBtn = createButton("Constants")

        self.menuBtn = createButton("Back to Menu")

        #The buttons' function are defined here

        def startExperiment_cb():
            if self.app.variablesInputted:
                if self.app.animationRunning == False:
                    self.app.animationRunning = True
                else:
                    gui.Dialog(gui.Label("ERROR"), gui.Label("Experiment already running"))
            else:
                gui.Dialog(gui.Label("ERROR"),gui.Label("You haven't set the variables"))

        self.startExperimentBtn.connect(gui.CLICK,startExperiment_cb)

        def pauseExperiment_cb():
            self.app.engine.clock.pause()

        self.pauseExperimentBtn.connect(gui.CLICK,pauseExperiment_cb)

        def menuBtn_cb():
            import MainMenu as m
            m.run()

        self.menuBtn.connect(gui.CLICK,menuBtn_cb)

        #Adding the buttons to the table
        self = addBtnToTbl(self,self.graphBtn)
        self = addBtnToTbl(self,self.variablesBtn)
        self = addBtnToTbl(self,self.startExperimentBtn)
        self = addBtnToTbl(self,self.pauseExperimentBtn)
        self = addBtnToTbl(self,self.restartExperimentBtn)
        self = addBtnToTbl(self,self.instructionBtn)
        self = addBtnToTbl(self,self.constantsBtn)
        self = addBtnToTbl(self,self.menuBtn)



class ExperimentTemplate(gui.Desktop):
    def __init__(self, screen):
        gui.Desktop.__init__(self)
        self.connect(gui.QUIT,self.quit)

        self.engine = None
        self.animationAreaWidth = 650
        self.animationAreaHeight = 400
        self.animationArea = DrawingArea(self.animationAreaWidth, self.animationAreaHeight)

        self.menuArea = MenuAreaTemplate(screen.get_width() - self.animationAreaWidth, self.animationAreaHeight, self)

        self.tableArea = TableAreaTemplate(screen.get_width(), 200, self)

        self.variablesInputted = False
        self.animationRunning = False
        self.experimentFinished = False

        screentbl = gui.Table()
        topTbl = gui.Table()
        topTbl.tr()
        topTbl.td(self.animationArea)
        topTbl.td(self.menuArea)
        screenTbl = gui.Table(height= screen.get_height(), width = screen.get_width())

        screenTbl.tr()
        screenTbl.td(topTbl)
        screenTbl.tr()
        screenTbl.td(self.tableArea)

        self.menuArea.setup()

        self.init(screenTbl, screen)

    def open(self, dlg: object, pos: object = None) -> object:  # Same method as found in gui18.py in the pgu examples
        self.animationArea.save_background()  # Pause the gameplay while the dialog is visible
        running = not (self.engine.clock.paused)
        self.engine.clock.pause()
        gui.Desktop.open(self, dlg, pos)
        while (dlg.is_open()):
            for ev in pygame.event.get():
                self.event(ev)
            rects = self.update()
            if (rects):
                pygame.display.update(rects)
            if (running):
                self.engine.clock.resume()  # Resume gameplay

    def get_render_area(self):
        return self.animationArea.get_abs_rect()


class AnimationEngineTemplate(object):
    def __init__(self, disp):
        self.disp = disp
        self.app = ExperimentTemplate(self.disp)
        self.app.engine = self

    def render(self, dest, rect):

        # Drawing code should go here

        return (rect,)

    def setupAnimation(self):
        # Called once the user has entered correct variables
        pass

    def run(self):  # This function is taken from the gui18.py which is in the pgu module under examples
        self.app.update(self.disp)
        pygame.display.flip()

        self.clock = timer.Clock()
        done = False

        while not done:
            for event in pygame.event.get():
                quitBool = (event.type == pygame.QUIT) or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
                if quitBool:
                    done = True
                else:
                    self.app.event(event)

            rect = self.app.get_render_area()
            updates = []
            self.disp.set_clip(rect)
            lst = self.render(self.disp, rect)
            if (lst):
                updates += lst

            self.disp.set_clip()
            # Cap it at 30fps
            self.clock.tick(30)

            # Give pgu a chance to update the display
            lst = self.app.update(self.disp)
            if (lst):
                updates += lst
            pygame.display.update(updates)
            pygame.time.wait(10)

        pygame.quit()

def createButton(text):
    return gui.Button(text,width = 225, height = 40)

def addBtnToTbl(tbl,btn):
    tbl.tr()
    tbl.td(btn)
    return tbl


def main(expName):
    disp = pygame.display.set_mode((900, 600))
    pygame.display.set_caption(expName)
    eng = AnimationEngineTemplate(disp)
    eng.run()
