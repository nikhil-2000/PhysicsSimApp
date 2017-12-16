import Experiments.ExperimentObjects as template
import externalModules.pgu.pgu.gui as gui
import Validation.validation as validation
import Experiments.creatingGraphs as graph
from externalModules.pgu.pgu import html
from Experiments.ResistivityOfAMetal.experiment import *
import webbrowser

class GraphDialog(gui.Dialog):
    def __init__(self,xPoints,yPoints):
        gradient,yIntercept = graph.createGraph(xPoints,yPoints,"Current Length/cm","Resistance/Ω")
        gradientLbl = gui.Label("Gradient:" + str(round(gradient,3)))
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
        self.minIVValue = None
        self.maxIVValue = None
        self.intervalValue = None
        self.defaultVals = defaultVals

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
         2. Start with crocodile clip at your starting value, record the current<br>
         3. Increase the length of the wire by moving the crocodile clip by your chosen interval<br>
         4. Once taking 5 or more results, divide the voltage by the current for each length. This gives the resistance<br>
         5. Now plot a graph for resistance(y-axis) against length(x-axis). The gradient will be equal to the resistance over the cross-sectional area"<br>
         6. Solve for the resistivity</li>
         </p>
         """
        #Adding the method to the document which html
        doc = html.HTML(method,width = 600)

        #Links to the useful websites
        link1 = "http://hyperphysics.phy-astr.gsu.edu/hbase/electric/resis.html"
        link2 = "http://hyperphysics.phy-astr.gsu.edu/hbase/Tables/rstiv.html"
        link3 = "http://papers.xtremepapers.com/CIE/Cambridge%20International%20A%20and%20AS%20Level/Physics%20(9702)/9702_nos_ps_9.pdf"

        #Linking websites to buttons
        def link1_cb():
            webbrowser.open(link1)

        def link2_cb():
            webbrowser.open(link2)

        def link3_cb():
            webbrowser.open(link3)

        btnWidth = 50
        btnHeight = 50
        link1Btn = gui.Button("About Resistance and Resistivity",width = 2*btnWidth, height=btnHeight)
        link1Btn.connect(gui.CLICK,link1_cb)
        link2Btn = gui.Button("Compare your Results",width = btnWidth, height=btnHeight)
        link2Btn.connect(gui.CLICK, link2_cb)
        link3Btn = gui.Button("Another Method",width = btnWidth, height=btnHeight)
        link3Btn.connect(gui.CLICK, link3_cb)

        #Adding buttons to the dialog
        tbl = gui.Table()
        tbl.tr()
        tbl.td(doc)
        tbl.tr()
        tbl.td(gui.Label("Links"))
        btnsTbl = gui.Table(width=200)
        btnsTbl.tr()
        btnsTbl.td(link3Btn)
        btnsTbl.td(link2Btn)
        btnsTbl.td(link1Btn)
        tbl.tr()
        tbl.td(btnsTbl)


        gui.Dialog.__init__(self,gui.Label("Instructions and Links"), tbl)

class ConstantsDialog(gui.Dialog):
    def __init__(self):
        #The controlled variables
        materialLbl = gui.Label("Material: Constantan")
        CSALbl = gui.Label("Cross-Sectional Area: 2.01 x 10^-8")
        voltageLbl = gui.Label("Voltage:"+str(voltage)+"V")
        #Adding the labels to the table
        tbl = gui.Table()
        tbl.tr()
        tbl.td(materialLbl)
        tbl.tr()
        tbl.td(CSALbl)
        tbl.tr()
        tbl.td(voltageLbl)

        gui.Dialog.__init__(self,gui.Label("Constants"),tbl)
