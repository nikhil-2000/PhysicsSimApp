import sys
import os

sys.path.append("../../")

import Experiments.ExperimentObjects as template
import externalModules.pgu.pgu.gui as gui
import Validation.validation as validation
from externalModules.pgu.pgu import html
import webbrowser
from Experiments.InternalResistance import experiment as exp


class GraphDialog(gui.Dialog):
    def __init__(self,app):
        self.app = app
        firstGraph = self.app.tableArea.voltageCurrentGraph
        secondGraph = self.app.tableArea.resistanceCurrentGraph
        firstGraph.drawGraph()
        secondGraph.drawGraph()

        s1 = self.createSection(firstGraph)
        s2 = self.createSection(secondGraph)

        subTbl = gui.Table(width = 640)
        subTbl.tr()
        subTbl.td(s1)
        subTbl.td(s2)



        tbl = gui.Table()
        tbl.tr()
        tbl.td(gui.Image("graphs.png"))
        tbl.tr()
        tbl.td(subTbl)

        gui.Dialog.__init__(self,gui.Label("Graphs"),tbl)

    def createSection(self,graph):
        graphDataTbl = gui.Table()
        gradient = round(graph.gradient)
        graphDataTbl.td(gui.Label("Gradient:"))
        graphDataTbl.td(gui.Label(str(gradient)))
        graphDataTbl.tr()
        yInt = round(graph.yInt)
        graphDataTbl.td(gui.Label("Y-Intercept:"))
        graphDataTbl.td(gui.Label(str(yInt)))

        tbl = gui.Table()
        tbl.tr()
        tbl.td(gui.Label(graph.graphName))
        tbl.tr()
        tbl.td(graphDataTbl)
        return tbl




class VariablesDialog(gui.Dialog):
    def __init__(self,defaultVals):
        #Object can tell menu that inputs are valid if isValidated is True
        self.isValidated = False
        #Allows menu object to access these variables one defined
        self.minIVValue = None
        self.maxIVValue = None
        self.intervalValue = None
        self.defaultVals = defaultVals

        #Explaining the paremeters of the input dialog
        explainLbl = gui.Label("Input your variables below")
        nOfResultsLbl = gui.Label("Have between 5-10 recordings")
        rangeStr = str("The range is " + str(exp.minRange) + " to " + str(exp.maxRange))
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
        minIVUnitLbl = gui.Label("Ω")
        maxIVUnitLbl = gui.Label("Ω")
        intervalIVUnitLbl = gui.Label("Ω")

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
            self.isValidated,error = validation.validateInputs(minIV,maxIV,interval,exp.maxRange,exp.minRange)
            if not self.isValidated:#If they aren't valid
                # Show error
                errorDlg = template.ErrorDlg(error)
                self.open(errorDlg)
            else:
                #Set object variables
                self.isValidated = True
                self.minIVValue = int(minIV)
                self.maxIVValue = int(maxIV)
                self.intervalValue = int(interval)
                self.close()

        def defaultBtn_cb():
            #A set of values if the user can't decide
            minIVUserInput.value = self.defaultVals[0]
            maxIVUserInput.value = self.defaultVals[1]
            intervalIVUserInput.value = self.defaultVals[2]

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
        #The method
        method = """<p>
         1. Set up the circuit as shown in the diagram<br>
         2. Start with crocodile clip at your 0 resistance, record the current<br>
         3. Increase the resistance by moving the crocodile clip<br>
         4. Once taking 5 or more results, multiply the resistance by the current for each recording. This gives the voltage<br>
         5. Now plot a graph for resistance(y-axis) against 1/Current(x-axis). The gradient will be the EMF and the internal resistance is the y-intercept"<br>
         6. Also plot a 2nd graph for Voltage(y-axis) against Current(x-axis). The gradient will be the internal resistance and the y-intercept is the EMF<br>
         </p>
         """
        #Adding the method to the document which html
        doc = html.HTML(method,width = 600)

        #Links to the useful websites
        link1 = "https://www.s-cool.co.uk/a-level/physics/resistance/revise-it/internal-resistance-emf-and-potential-difference"
        link2 = "http://physicsnet.co.uk/a-level-physics-as-a2/current-electricity/electromotive-force-and-internal-resistance/"
        link3 = "http://personal.psu.edu/bqw/physics_151/lab/lab151_5.html"
        pdf = "file:///D:/My%20Docs/School/Computer%20Science/Programming%20Project/physicssimulationapp/resources/Methods/DeterminationOfTheInternalResistanceOfACell.pdf"
        chrome = "C:\Program Files (x86)\Google\Chrome\chrome.exe"

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
        link1Btn = gui.Button("The Theory behind the Experiment",width = 2*btnWidth, height=btnHeight)
        link1Btn.connect(gui.CLICK,link1_cb)
        link2Btn = gui.Button("More Theory",width = btnWidth, height=btnHeight)
        link2Btn.connect(gui.CLICK, link2_cb)
        link3Btn = gui.Button("Another Method",width = btnWidth, height=btnHeight)
        link3Btn.connect(gui.CLICK, link3_cb)
        link4Btn = gui.Button("Eduqas Practical Sheet", width=2*btnWidth, height=btnHeight)
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
        lbl1 = gui.Label("The equations below show the line the equation for the graphs")
        lbl2 = gui.Label("Using the graphs, determine values for the EMF and internal resistance of this battery")
        dataTbl = gui.Table()
        dataTbl.tr()
        dataTbl.td(lbl1)
        dataTbl.tr()
        dataTbl.td(lbl2)


        #The equation needed
        equationImg = gui.Image("internalResistanceEquations.png")
        imgTable = gui.Table()
        imgTable.td(equationImg)

        #The question
        questionLbl = gui.Label("Enter the values for EMF and internal resistance")
        questionTable = gui.Table()
        questionTable.tr()
        questionTable.td(questionLbl)
        questionTable.tr()

        #The Options for answers
        answerTbl = gui.Table()
        EMFLbl = gui.Label("EMF")
        EMFAns = gui.Input()
        internalRLbl = gui.Label("Internal Resistance")
        internalRAns = gui.Input()
        answerTbl.tr()
        answerTbl.td(EMFLbl,style = tdStyle)
        answerTbl.td(EMFAns)
        answerTbl.tr()
        answerTbl.td(internalRLbl)
        answerTbl.td(internalRAns,style = tdStyle)



        #Checking User Answers
        checkAnswerBtn = gui.Button("Check Answer",width=100,height=30)

        def checkAnswer():
            if EMFAns.value == str(exp.EMF) and internalRAns.value == str(exp.internalResistance):
                dlg = gui.Dialog(gui.Label("Your answers were..."),gui.Label("Correct. Well Done"))
            else:
                dlg = gui.Dialog(gui.Label("Your answers were..."),gui.Label("Wrong. Try Again"))

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
