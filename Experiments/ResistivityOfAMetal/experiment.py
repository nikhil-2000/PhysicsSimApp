import os
import sys
from externalModules.pgu.pgu import gui
from externalModules.pgu.pgu import html
sys.path.append(os.path.abspath('..'))

import Experiments.ExperimentObjects as template
import Experiments.creatingGraphs as graph
import pygame
import math
import Validation.validation as validation
import webbrowser
import resources.Colour as colours

csa = round(2.01 * 10 ** -8,10)
voltage = 1.5


class GraphDialog(gui.Dialog):
    def __init__(self,xPoints,yPoints):
        gradient,yIntercept = graph.createGraph(xPoints,yPoints)
        gradientLbl = gui.Label(str(round(gradient,3)))
        yInterceptLbl = gui.Label(str(round(yIntercept,3)))

        tbl = gui.Table()
        tbl.tr()
        tbl.td(gui.Image("graph.png"))
        tbl.tr()
        tbl.td(gradientLbl)
        tbl.tr()
        tbl.td(yInterceptLbl)

        gui.Dialog.__init__(self,gui.Label("Graph"),tbl)

class VariablesDialog(gui.Dialog):
    def __init__(self,defaultVals,minRange,maxRange):
        #Object can tell menu that inputs are valid if isValidated is True
        self.isValidated = False
        #Allows menu object to access these variables one defined
        self.minIVValue = None
        self.maxIVValue = None
        self.intervalValue = None

        #Explaining the paremeters of the input dialog
        explainLbl = gui.Label("Input your variables below")
        nOfResultsLbl = gui.Label("Have between 5-10 recordings")
        rangeStr = str("The range is " + str(minRange) + " to " + str(maxRange))
        rangeLbl = gui.Label(rangeStr)

        #THe labels for each input
        minIVUserLbl = gui.Label("Min")
        maxIVUserLbl = gui.Label("Max")
        intervalUserLbl = gui.Label("Interval")

        #The input boxes
        minIVUserInput = gui.Input()
        maxIVUserInput = gui.Input()
        intervalIVUserInput = gui.Input()

        #The units for each input
        minIVUnitLbl = gui.Label("cm")
        maxIVUnitLbl = gui.Label("cm")
        intervalIVUnitLbl = gui.Label("cm")

        #Standard width and height for buttons in this dialog
        buttonHeight = 50
        buttonWidth = 120

        #Making buttons then giving them functions
        okBtn = gui.Button("Enter",height=buttonHeight, width=buttonWidth)
        defaultBtn = gui.Button("Default Values",height=buttonHeight, width=buttonWidth)

        def okBtn_cb():
            #Takes currently inputted values
            minIV = minIVUserInput.value
            maxIV = maxIVUserInput.value
            interval = intervalIVUserInput.value

            #Runs through validation algorithm
            self.isValidated,error = validation.validateInputs(minIV,maxIV,interval,maxRange,minRange)
            if not self.isValidated:#If they aren't valid
                # Show error
                errorDlg = template.ErrorDlg(error)
                errorDlg.open()
            else:
                #Set object variables
                self.isValidated = True
                self.minIVValue = minIV
                self.maxIVValue = maxIV
                self.intervalValue = interval

        def defaultBtn_cb():
            #A set of values if the user can't decide
            minIVUserInput.value = 10
            maxIVUserInput.value = 100
            intervalIVUserInput.value = 10

        #Links buttons with functions on click
        okBtn.connect(gui.CLICK,okBtn_cb)
        defaultBtn.connect(gui.CLICK,defaultBtn_cb)

        #Wraps all widgets into tables then put into one large table
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

class InstructionsLinkDialog(gui.Dialog):
    def __init__(self):
        method = """<p> 1. Set up the circuit as shown in the diagram<br>
         2. Start with crocodile clip at your starting value, record the current<br>
         3. Increase the length of the wire by moving the crocodile clip by your chosen interval<br>
         4. Once taking 5 or more results, divide the voltage by the current for each length. This gives the resistance"<br>
         5. Now plot a graph for resistance(y-axis) against length(x-axis). The gradient will be equal to th resistance over the cross-sectional area"<br>
         6. Solve for the resistivity<p>
         """
        doc = html.HTML(method,width = 600)

        link1 = "http://hyperphysics.phy-astr.gsu.edu/hbase/electric/resis.html"
        link2 = "http://hyperphysics.phy-astr.gsu.edu/hbase/Tables/rstiv.html"
        link3 = "http://papers.xtremepapers.com/CIE/Cambridge%20International%20A%20and%20AS%20Level/Physics%20(9702)/9702_nos_ps_9.pdf"

        def link1_cb():
            webbrowser.open(link1)

        def link2_cb():
            webbrowser.open(link2)

        def link3_cb():
            webbrowser.open(link3)

        link1Btn = gui.Button("About Resistance and Resistivity")
        link1Btn.connect(gui.CLICK,link1_cb)
        link2Btn = gui.Button("Compare your Results")
        link2Btn.connect(gui.CLICK, link2_cb)
        link3Btn = gui.Button("Another Method")
        link3Btn.connect(gui.CLICK, link3_cb)

        tbl = gui.Table()
        tbl.tr()
        tbl.td(doc)
        tbl.tr()
        tbl.td(gui.Label("Links"))
        tbl.tr()
        tbl.td(link1Btn)
        tbl.tr()
        tbl.td(link2Btn)
        tbl.tr()
        tbl.td(link3Btn)


        gui.Dialog.__init__(self,gui.Label("Instructions and Links"), tbl)

class ConstantsDialog(gui.Dialog):
    def __init__(self):
        materialLbl = gui.Label("Material: Constantan")

        CSALbl = gui.Label("Cross-Sectional Area: 2.01 x 10^-8")
        voltageLbl = gui.Label("Voltage:"+str(voltage)+"V")

        tbl = gui.Table()
        tbl.tr()
        tbl.td(materialLbl)
        tbl.tr()
        tbl.td(CSALbl)
        tbl.tr()
        tbl.td(voltageLbl)

        gui.Dialog.__init__(self,gui.Label("Constants"),tbl)



class TableArea(template.TableAreaTemplate):
    def __init__(self,width,height,app):
        super(TableArea, self).__init__(width,height,app)


class MenuArea(template.MenuAreaTemplate):
    def __init__(self,width,height,app):
        super(MenuArea, self).__init__(width,height,app)
        self.setupButtons()

    def setupButtons(self):
        self.setup()

        def graph_cb():
            if self.app.experimentFinished:
                graphDlg = GraphDialog(xPoints,yPoints)
                self.open(graphDlg)
            else:
                errorDlg = template.ErrorDlg("Finish the Experiment")
                self.app.open(errorDlg)

        self.graphBtn.connect(gui.CLICK,graph_cb)

        def variables_cb():
            variablesDlg = VariablesDialog(["10,100,10"],0,100)
            variablesDlg.open()

        self.variablesBtn.connect(gui.CLICK,variables_cb)

        def constant_cb():
            constantsDlg = ConstantsDialog()
            self.open(constantsDlg)

        self.constantsBtn.connect(gui.CLICK,constant_cb)

        def instructions_cb():
            instructionsDlg = InstructionsLinkDialog()
            self.open(instructionsDlg)

        self.instructionBtn.connect(gui.CLICK,instructions_cb)

class Experiment(template.ExperimentTemplate):
    def __init__(self,screen):
        super(Experiment, self).__init__(screen)
        gui.Desktop.__init__(self)
        self.connect(gui.QUIT,self.quit)

        self.engine = None
        self.animationAreaWidth = 650
        self.animationAreaHeight = 400
        self.animationArea = template.DrawingArea(self.animationAreaWidth, self.animationAreaHeight)

        self.menuArea = MenuArea(screen.get_width() - self.animationAreaWidth, self.animationAreaHeight, self)

        self.tableArea = TableArea(screen.get_width(), 200, self)

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

        self.init(screenTbl, screen)

class AnimationEngine(template.AnimationEngineTemplate):
    def __init__(self, disp):
        super(AnimationEngine, self).__init__(disp)
        self.app = Experiment(self.disp)
        self.app.engine = self

    def render(self, dest, rect):

        return (rect,)


def run():
    disp = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("Determination of the Resistivity of a Metal")
    eng = AnimationEngine(disp)
    eng.run()



if __name__ == '__main__':
    run()
