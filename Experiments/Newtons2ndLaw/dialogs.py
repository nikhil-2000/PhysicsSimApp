import sys
import os

sys.path.append("../../")

import Experiments.ExperimentObjects as template
import externalModules.pgu.pgu.gui as gui
import Validation.validation as validation
from externalModules.pgu.pgu import html
import webbrowser
from Experiments.Newtons2ndLaw import experiment as exp
import Experiments.creatingGraphs as graph
import resources.resourceManager as resM


class GraphDialog(gui.Dialog):
    def __init__(self,table):
        self.tableArea = table
        xPoints = self.tableArea.xPoints
        yPoints = self.tableArea.yPoints
        gradient,yIntercept = graph.createGraph(xPoints,yPoints,"Weight Force of Mass Holder/N","Acceleration/(m/s²)")
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
        #Allows menu object to access these variables one defined
        self.cartWeights = None
        self.massHolderWeights = None
        self.weightSize = None
        self.defaultVals = defaultVals

        #Explaining the paremeters of the input dialog
        explainLbl = gui.Label("Input your variables below")
        nOfResultsLbl = gui.Label("Have between 5-10 recordings")
        rangeStr = str("The weight range is " + str(exp.minRange) + " to " + str(exp.maxRange))
        rangeLbl = gui.Label(rangeStr)


        #THe labels for each input
        minIVUserLbl = gui.Label("Weights on Cart")
        maxIVUserLbl = gui.Label("Weights on Mass Holder")

        #The input boxes
        # The Options for answers
        optionsTbl = gui.Table()
        optionsGroup = gui.Group()
        intervalUserLbl = gui.Label("Weights on Mass Holder")
        FiftygLbl = gui.Label("50g")
        FiftygCheckBox = gui.Radio(optionsGroup, value=1)
        HundredgLbl = gui.Label("100g")
        HundredgCheckBox = gui.Radio(optionsGroup, value=2)
        TwoHundredgLbl = gui.Label("150g")
        TwoHundredgCheckBox = gui.Radio(optionsGroup, value=3)

        tdStyle = {'padding': 10}
        optionsTbl.td(intervalUserLbl, style=tdStyle)
        optionsTbl.td(FiftygLbl, style=tdStyle)
        optionsTbl.td(FiftygCheckBox)
        optionsTbl.td(HundredgLbl, style=tdStyle)
        optionsTbl.td(HundredgCheckBox)
        optionsTbl.td(TwoHundredgLbl, style=tdStyle)
        optionsTbl.td(TwoHundredgCheckBox)

        maxIVUserInput = gui.Input()
        minIVUserInput = gui.Input()

        #The units for each input
        maxIVUnitLbl = gui.Label("g")
        minIVUnitLbl = gui.Label("g")

        #Standard width and height for buttons in this dialog
        buttonHeight = 50
        buttonWidth = 120

        #Making buttons then giving them functions
        okBtn = gui.Button("Enter",height=buttonHeight, width=buttonWidth)
        defaultBtn = gui.Button("Default Values",height=buttonHeight, width=buttonWidth)

        def okBtn_cb():
            #Takes currently inputted values
            if optionsGroup.value == 1:
                interval = "50"
            elif optionsGroup.value == 2:
                interval = "100"
            elif optionsGroup.value == 3:
                interval = "150"
            else:
                interval = ""


            cartWeights = minIVUserInput.value
            massHolderWeights = maxIVUserInput.value

            #Runs through validation algorithm
            self.isValidated,error = validation.validateNewton2ndLaw(cartWeights,massHolderWeights,interval,exp.minRange,exp.maxRange)
            if not self.isValidated:#If they aren't valid
                # Show error
                errorDlg = template.ErrorDlg(error)
                self.open(errorDlg)
            else:
                #Set object variables
                self.isValidated = True
                self.cartWeights = int(cartWeights)
                self.massHolderWeights = int(massHolderWeights)
                self.weightSize = round(int(interval) /1000,2)

                self.close()

        def defaultBtn_cb():
            #A set of values if the user can't decide
            optionsGroup.value = 2
            minIVUserInput.value = self.defaultVals[1]
            maxIVUserInput.value = self.defaultVals[2]

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

        buttonTbl.tr()
        buttonTbl.td(okBtn,style=inputTblStyle)
        buttonTbl.td(defaultBtn,style=inputTblStyle)

        tbl = gui.Table()
        tbl.tr()
        tbl.td(textTbl)
        tbl.tr()
        tbl.td(inputTbl)
        tbl.tr()
        tbl.td(optionsTbl)
        tbl.tr()
        tbl.td(buttonTbl)


        gui.Dialog.__init__(self,gui.Label("Variables"),tbl)



class InstructionsLinkDialog(gui.Dialog):
    def __init__(self):
        #The method
        method = """<p>
         1. Set up the equipment as shown in the diagram<br>
         2. Place all the weights on the cart<br>
         3. Release the cart, the cart should begin to move<br>
         4. The two light gates will record the velocity which can be used to calculate the acceleration of the cart<br>
         5. Then move a mass from the cart to the mass holder and repeat step 3-4<br>
         6. Once all the weights have been transferred, plot a graph of mg against a where m is the mass on the hanger and a is the acceleration of the cart<br>
         </p>
         """
        #Adding the method to the document which html
        doc = html.HTML(method,width = 600)

        #Links to the useful websites
        link1 = "http://www.physicsandmathstutor.com/physics-revision/a-level-wjec-eduqas/component-1/"
        link2 = "http://www.physicsclassroom.com/class/newtlaws/Lesson-3/Newton-s-Second-Law"
        link3 = "http://practicalphysics.org/investigating-newtons-second-law-motion.html"
        pdf = "file:///D:/My%20Docs/School/Computer%20Science/Programming%20Project/physicssimulationapp/resources/Methods/Investigation%20of%20Newton's%20second%20law.pdf"

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
        link1Btn = gui.Button("Questions for Forces",width = btnWidth, height=btnHeight)
        link1Btn.connect(gui.CLICK,link1_cb)
        link2Btn = gui.Button("Newton's 2nd Law",width = btnWidth, height=btnHeight)
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
        imgTable.td(gui.Image(resM.newtons2ndLawEquation))

        #The question
        questionLbl = gui.Label("What does the k represent?")
        questionTable = gui.Table()
        questionTable.tr()
        questionTable.td(questionLbl)

        #The Options for answers
        optionsTbl = gui.Table()
        optionsGroup = gui.Group()
        correctAnswer = gui.Label("1/(M+m)")
        correctAnswerCheckBox = gui.Radio(optionsGroup,value=1)
        incorrectAnswer1 = gui.Label("M+m")
        incorrectAnswer1CheckBox = gui.Radio(optionsGroup,value=2)
        incorrectAnswer2 = gui.Label("M")
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