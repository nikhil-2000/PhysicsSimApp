import sys
import os

sys.path.append("../../")

import Experiments.ExperimentObjects as template
import externalModules.pgu.pgu.gui as gui
import Validation.validation as validation
from externalModules.pgu.pgu import html
import webbrowser
from Experiments.RadioactiveDecay import experiment as exp
import resources.resourceManager as resM


class GraphDialog(gui.Dialog):
    def __init__(self,tableArea):

        firstGraph = tableArea.exponentialGraph
        secondGraph = tableArea.lnGraph
        firstGraph.drawGraph(True)
        secondGraph.drawGraph(False)

        s1 = self.createSection(firstGraph,True)
        s2 = self.createSection(secondGraph,False)

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

    def createSection(self,graph,isExponential):
        graphDataTbl = gui.Table()
        gradient = graph.gradient
        graphDataTbl.td(gui.Label("Gradient:"))
        graphDataTbl.td(gui.Label(str(gradient)))
        graphDataTbl.tr()
        yInt = graph.yInt
        graphDataTbl.td(gui.Label("Y-Intercept:"))
        graphDataTbl.td(gui.Label(str(yInt)))

        tbl = gui.Table()
        tbl.tr()
        tbl.td(gui.Label(graph.graphName))
        if not isExponential:
            tbl.tr()
            tbl.td(graphDataTbl)

        return tbl



class VariablesDialog(gui.Dialog):
    def __init__(self,defaultVals):
        #Object can tell menu that inputs are valid if isValidated is True
        self.isValidated = False
        #Allows menu object to access these variables one defined
        self.startTime = None
        self.endTime = None
        self.timeInterval = None
        self.defaultVals = defaultVals

        #Explaining the paremeters of the input dialog
        explainLbl = gui.Label("Input your variables below")
        nOfResultsLbl = gui.Label("Have between 5-10 recordings")
        rangeStr = str("The time range is " + str(exp.minRange) + " to " + str(exp.maxRange))
        rangeLbl = gui.Label(rangeStr)

        # THe labels for each input
        minIVUserLbl = gui.Label("Start Time")
        maxIVUserLbl = gui.Label("End Time")
        intervalUserLbl = gui.Label("Time Interval")

        # The input boxes
        minIVUserInput = gui.Input()
        maxIVUserInput = gui.Input()
        intervalIVUserInput = gui.Input()

        # The units for each input
        minIVUnitLbl = gui.Label("s")
        maxIVUnitLbl = gui.Label("s")
        intervalIVUnitLbl = gui.Label("s")

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
            isValidated,error = validation.validateInputs(minIV,maxIV,interval,exp.maxRange,exp.minRange)


            if not isValidated:#If they aren't valid
                # Show error
                errorDlg = template.ErrorDlg(error)
                self.open(errorDlg)
            else:
                if int(maxIV) - int(minIV) >= 200:
                    #Set object variables
                    self.isValidated = True
                    self.startTime = int(minIV)
                    self.endTime = int(maxIV)
                    self.timeInterval = int(interval)
                    self.close()
                else:
                    errorDlg = template.ErrorDlg("Make the range at least 200")
                    self.open(errorDlg)

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
         1. This experiment is dependent on observations rather than a practical method<br>
         2. The radioactive isotope shown is to be determined by you<br>
         3. The undecayed nuclei will be red while the decayed are yellow<br>
         4. When this isotope decays, it releases a electron and increases the proton number by one<br>
         5. Therefore it is beta decay<br>
         6. Take regular recordings of the number of undecayed nuclei<br>
         7. Plot the ln(n of undecayed nuclei) against the time(x-axis)<br>
         8. Rearrange and use the gradient to find the decay constant
         </p>
         """
        #Adding the method to the document which html
        doc = html.HTML(method,width = 600)

        #Links to the useful websites
        link1 = "https://en.wikipedia.org/wiki/List_of_radioactive_isotopes_by_half-life#100_seconds"
        link2 = "http://www.a-levelphysicstutor.com/nucphys-radioactivity.php"
        link3 = "https://phet.colorado.edu/en/simulation/alpha-decay"
        pdf = "file:///D:/My%20Docs/School/Computer%20Science/Programming%20Project/physicssimulationapp/resources/Methods/RadioactiveDecay.pdf"

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
        link1Btn = gui.Button("List of Radioactive Isotopes",width = btnWidth, height=btnHeight)
        link1Btn.connect(gui.CLICK,link1_cb)
        link2Btn = gui.Button("Information on Radioactivity",width = btnWidth, height=btnHeight)
        link2Btn.connect(gui.CLICK, link2_cb)
        link3Btn = gui.Button("Alternative Simulation",width = btnWidth, height=btnHeight)
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
        equationImg = gui.Image(resM.radioactiveDecayEquations)
        imgTable = gui.Table()
        imgTable.td(equationImg)

        #The question
        questionLbl = gui.Label("Which radioactive isotope was used in this experiment?")
        questionTable = gui.Table()
        questionTable.tr()
        questionTable.td(questionLbl)

        #The Options for answers
        optionsTbl = gui.Table()
        optionsGroup = gui.Group()
        correctAnswer = gui.Label("Fermium - 252")
        correctAnswerCheckBox = gui.Radio(optionsGroup,value=1)
        incorrectAnswer1 = gui.Label("Gold - 196")
        incorrectAnswer1CheckBox = gui.Radio(optionsGroup,value=2)
        incorrectAnswer2 = gui.Label("Uranium - 236")
        incorrectAnswer2CheckBox = gui.Radio(optionsGroup,value=3)

        tdStyle = {'padding':10}
        optionsTbl.td(incorrectAnswer1,style = tdStyle)
        optionsTbl.td(incorrectAnswer2,style = tdStyle)
        optionsTbl.td(correctAnswer,style = tdStyle)
        optionsTbl.tr()
        optionsTbl.td(incorrectAnswer1CheckBox)
        optionsTbl.td(incorrectAnswer2CheckBox)
        optionsTbl.td(correctAnswerCheckBox)



        #Checking User Answers
        checkAnswerBtn = gui.Button("Check Answer",width=100,height=30)

        def checkAnswer():
            if optionsGroup.value == 1:
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
        tbl.td(optionsTbl,style = tdStyle)
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