import sys
import os

sys.path.append("../../")

import Experiments.ExperimentObjects as template
import externalModules.pgu.pgu.gui as gui
import Validation.validation as validation
from externalModules.pgu.pgu import html
import webbrowser
from Experiments.Measureg import experiment as exp
import Experiments.creatingGraphs as graph
import resources.resourceManager as resM


class GraphDialog(gui.Dialog):
    def __init__(self,table):
        self.tableArea = table
        xPoints = self.tableArea.xPoints
        yPoints = self.tableArea.yPoints
        gradient,yIntercept = graph.createGraph(xPoints,yPoints,"Height/m","Time²/s²")
        gradientLbl = gui.Label("Gradient:" + str(round(gradient,6)))
        yInterceptLbl = gui.Label("Y-Intercept:" + str(round(yIntercept,3)))

        tbl = gui.Table()
        tbl.tr()
        tbl.td(gui.Image("graph.png"))
        tbl.tr()
        tbl.td(gradientLbl)
        tbl.tr()
        tbl.td(yInterceptLbl)

        gui.Dialog.__init__(self,gui.Label("Graph"),tbl)


class VariablesDialog(gui.Dialog):
    def __init__(self,defaultVals):
        #Object can tell menu that inputs are valid if isValidated is True
        self.isValidated = False
        #Creates variables to be accessed once defined
        self.startHeight = None
        self.endHeight = None
        self.heightInterval = None
        self.defaultVals = defaultVals

        #Explaining the paremeters of the input dialog
        explainLbl = gui.Label("Input your variables below")
        nOfResultsLbl = gui.Label("Have between 5-10 recordings")
        rangeStr = str("The height range is " + str(exp.minRange) + "cm to " + str(exp.maxRange) + "cm")
        rangeLbl = gui.Label(rangeStr)

        # THe labels for each input
        minIVUserLbl = gui.Label("Start Height")
        maxIVUserLbl = gui.Label("End Height")
        intervalUserLbl = gui.Label("Height Interval")

        # The input boxes
        minIVUserInput = gui.Input()
        maxIVUserInput = gui.Input()
        intervalIVUserInput = gui.Input()

        # The units for each input
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
            # Takes currently inputted values
            minIV = minIVUserInput.value
            maxIV = maxIVUserInput.value
            interval = intervalIVUserInput.value

            # Runs through validation algorithm
            isValidated, error = validation.validateInputs(minIV, maxIV, interval, exp.maxRange, exp.minRange)

            if not isValidated:#If they aren't valid
                # Show error
                errorDlg = template.ErrorDlg(error)
                self.open(errorDlg)
            else:
                #Set object variables
                self.isValidated = True
                self.startHeight = int(minIV)
                self.endHeight = int(maxIV)
                self.heightInterval = int(interval)

                self.close()

        def defaultBtn_cb():
            #A set of values if the user can't decide
            minIVUserInput.value = self.defaultVals[0]
            maxIVUserInput.value = self.defaultVals[1]
            intervalIVUserInput.value = self.defaultVals[2]


        #Links buttons with functions on click
        okBtn.connect(gui.CLICK,okBtn_cb)
        defaultBtn.connect(gui.CLICK,defaultBtn_cb)

        # Wraps all widgets into tables then put into one large table
        textTbl = gui.Table()
        inputTbl = gui.Table()
        buttonTbl = gui.Table()

        textTbl.tr()
        textTbl.td(explainLbl)
        textTbl.tr()
        textTbl.td(nOfResultsLbl)
        textTbl.tr()
        textTbl.td(rangeLbl)

        inputTblStyle = {'padding': 10}
        inputTbl.tr()
        inputTbl.td(minIVUserLbl, style=inputTblStyle)
        inputTbl.td(minIVUserInput, style=inputTblStyle)
        inputTbl.td(minIVUnitLbl, style=inputTblStyle)
        inputTbl.tr()
        inputTbl.td(maxIVUserLbl, style=inputTblStyle)
        inputTbl.td(maxIVUserInput, style=inputTblStyle)
        inputTbl.td(maxIVUnitLbl, style=inputTblStyle)
        inputTbl.tr()
        inputTbl.td(intervalUserLbl, style=inputTblStyle)
        inputTbl.td(intervalIVUserInput, style=inputTblStyle)
        inputTbl.td(intervalIVUnitLbl, style=inputTblStyle)

        buttonTbl.tr()
        buttonTbl.td(okBtn, style=inputTblStyle)
        buttonTbl.td(defaultBtn, style=inputTblStyle)

        tbl = gui.Table()
        tbl.tr()
        tbl.td(textTbl)
        tbl.tr()
        tbl.td(inputTbl)
        tbl.tr()
        tbl.td(buttonTbl)

        gui.Dialog.__init__(self, gui.Label("Variables"), tbl)



class InstructionsLinkDialog(gui.Dialog):
    def __init__(self):
        #The method
        method = """<p>
         1. Set up the equipment as shown in the diagram<br>
         2. Release the ball from start height<br>
         3. Measure the time taken for the ball to drop to the floor<br>
         4. Increase the height by the your interval and repeat steps 2-3<br>
         5. After testing for the final height, plot a graph of height(x-axis) against t²(y-axis)<br>
         6. Use the gradient of the graph to determine g<br>
         </p>
         """
        #Adding the method to the document which html
        doc = html.HTML(method,width = 700)

        #Links to the useful websites
        link1 = "http://www.physicsclassroom.com/class/1DKin/Lesson-5/Representing-Free-Fall-by-Graphs"
        link2 = "http://www.physicsclassroom.com/class/1DKin/Lesson-5/Acceleration-of-Gravity"
        link3 = "http://practicalphysics.org/investigating-free-fall-light-gate.html"
        pdf = "file:///D:/My%20Docs/School/Physics/Teacher%20-%20technician%20guidance%20for%20specified%20practicals/Measurement%20of%20g%20by%20freefall.pdf"

        #Linking websites to buttons
        def link1_cb():
            webbrowser.open(link1)

        def link2_cb():
            webbrowser.open(link2)

        def link3_cb():
            webbrowser.open(link3)

        def link4_cb():
            webbrowser.open(pdf)

        btnWidth = 200
        btnHeight = 50
        link1Btn = gui.Button("Freefall Graphs",width = btnWidth, height=btnHeight)
        link1Btn.connect(gui.CLICK,link1_cb)
        link2Btn = gui.Button("Information on acceleration due to gravity",width = btnWidth, height=btnHeight)
        link2Btn.connect(gui.CLICK, link2_cb)
        link3Btn = gui.Button("Alternative Method",width = btnWidth, height=btnHeight)
        link3Btn.connect(gui.CLICK, link3_cb)
        link4Btn = gui.Button("Eduqas Practical Sheet", width=btnWidth, height=btnHeight)
        link4Btn.connect(gui.CLICK, link4_cb)

        #Adding buttons to the dialog
        tbl = gui.Table()
        tbl.tr()
        tbl.td(doc)
        tbl.tr()
        tbl.td(gui.Label("Links"))
        topBtnTbl = gui.Table()
        topBtnTbl.tr()
        topBtnTbl.td(link2Btn)
        topBtnTbl.td(link1Btn)
        bottomBtnTbl = gui.Table()
        bottomBtnTbl.tr()
        bottomBtnTbl.td(link3Btn)
        bottomBtnTbl.td(link4Btn)
        tbl.tr()
        tbl.td(topBtnTbl)
        tbl.tr()
        tbl.td(bottomBtnTbl)

        gui.Dialog.__init__(self,gui.Label("Instructions and Links"), tbl)

class Questions(gui.Dialog):
    def __init__(self,app):
        #Needs access to the app use open method
        self.app = app
        tdStyle = {'padding':10}

        #The controlled variables
        lbl1 = gui.Label("The equations below show the line the equation for the graph")
        dataTbl = gui.Table()
        dataTbl.tr()
        dataTbl.td(lbl1)

        #The equation needed
        equationImg = gui.Image(resM.absoluteZero)
        imgTable = gui.Table()
        imgTable.td(gui.Image(resM.measuregEquation))

        #The question
        questionLbl = gui.Label("What is g to 2dp?")
        questionTable = gui.Table()
        questionTable.tr()
        questionTable.td(questionLbl)

        #The Options for answers
        answerTbl = gui.Table()
        gLbl = gui.Label("g")
        gAns = gui.Input()
        answerTbl.tr()
        answerTbl.td(gLbl)
        answerTbl.td(gAns,style = tdStyle)



        #Checking User Answers
        checkAnswerBtn = gui.Button("Check Answer",width=100,height=30)

        def checkAnswer():
            if gAns.value == "9.81":
                dlg = gui.Dialog(gui.Label("Your answer was..."),gui.Label("Correct. Well Done"))
            else:
                dlg = gui.Dialog(gui.Label("Your answer was..."),gui.Label("Wrong. Try Again"))

            self.app.open(dlg)

        checkAnswerBtn.connect(gui.CLICK,checkAnswer)

        #Adding the labels to the table
        tbl = gui.Table()
        tbl.tr()
        tbl.td(dataTbl,style = tdStyle)
        tbl.tr()
        tbl.td(imgTable,style = tdStyle)
        tbl.tr()
        tbl.td(questionTable,style = tdStyle)
        tbl.tr()
        tbl.td(answerTbl,style = tdStyle)
        tbl.tr()
        tbl.td(checkAnswerBtn,style = tdStyle)


        gui.Dialog.__init__(self,gui.Label("Question"),tbl)

class OptionsDialog(gui.Dialog):
    def __init__(self,app):
        self.app = app
        menuBtn = gui.Button("Back to Menu",width = 200,height=50)

        restartBtn = gui.Button("Restart Experiment",width = 200,height=50)

        def restartExperimentBtn_cb():
            self.app.restart()

        restartBtn.connect(gui.CLICK, restartExperimentBtn_cb)

        def menuBtn_cb():
            import MainMenu as m
            m.run()

        menuBtn.connect(gui.CLICK, menuBtn_cb)
        tbl = gui.Table()
        tbl.tr()
        tbl.td(menuBtn)
        tbl.tr()
        tbl.td(restartBtn)

        gui.Dialog.__init__(self,gui.Label("Options"),tbl)


def createButton(text):
    return gui.Button(text, width=225, height=40)

def addBtnToTbl(tbl, btn):
    tbl.tr()
    tbl.td(btn)
    return tbl