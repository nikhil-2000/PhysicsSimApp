from Experiments.Newtons2ndLaw import experiment as exp
import resources.Colour as colours
from resources.Equipment.ElectricalComponents import *
from Experiments.Newtons2ndLaw import dialogs as dlgs
from Experiments import ExperimentObjects as template
import externalModules.pgu.pgu.gui as gui
import resources.Equipment.PressureEquipment as pEquip


class TableArea(template.TableAreaTemplate):
    def __init__(self,width,height,app):
        super(TableArea, self).__init__(width,height,app)
        self.xPoints = []
        self.yPoints = []
        self.currentColumn = 1

    def setup(self):
        minIV = self.app.minIV
        maxIV = self.app.maxIV
        interval = self.app.interval

        cellStyle = {'border':1}

        currentNum = minIV
        self.tr()
        self.td(gui.Label("Temperature/°C"),style = cellStyle)
        while currentNum <= maxIV:
            self.xPoints.append(int(currentNum))
            lbl = gui.Label(str(currentNum))
            self.td(lbl,style = cellStyle)
            currentNum += interval


        self.tr()
        self.td(gui.Label("Pressure/kPa"),style = cellStyle)


    def addToTable(self,pressure):
        pressureLbl = gui.Label(str(round(pressure,2)))                                           #Round the values to make
        self.app.tableArea.td(pressureLbl, col=self.currentColumn, row=1, style={'border': 1})   #Adding the values
        self.yPoints.append(pressure)#Adds the unrounded values to y-points
        self.currentColumn += 1 # Increments columnCount for the add next value



class MenuArea(template.MenuAreaTemplate):
    def __init__(self,width,height,app):
        super(MenuArea, self).__init__(width,height,app)
        self.variablesDlg = dlgs.VariablesDialog(["20","65","5"])
        self.setupButtons()


    def setupButtons(self):
        self.setup()

        def graph_cb():
            if self.app.experimentFinished:
                graphDlg = dlgs.GraphDialog(self.app.tableArea)
                self.open(graphDlg)
            else:
                errorDlg = template.ErrorDlg("Finish the Experiment")
                self.app.open(errorDlg)


        self.graphBtn.connect(gui.CLICK,graph_cb)

        def variables_cb():
            if not self.app.variablesInputted:
                self.variablesDlg.open()
                if self.variablesDlg.isValidated:
                    #Updates the values of the Experiment Object
                    self.app.variablesInputted = True
                    self.app.minIV = self.variablesDlg.minIVValue
                    self.app.maxIV = self.variablesDlg.maxIVValue
                    self.app.interval = self.variablesDlg.intervalValue
                    self.app.tableArea.setup()
            else:
                self.app.open(template.ErrorDlg("You have already inputted variables."))

        self.variablesBtn.connect(gui.CLICK,variables_cb)

        def question():
            questions = dlgs.Questions(self.app)
            self.open(questions)

        self.questionBtn.connect(gui.CLICK,question)

        def instructions_cb():
            instructionsDlg = dlgs.InstructionsLinkDialog()
            self.open(instructionsDlg)

        self.instructionBtn.connect(gui.CLICK,instructions_cb)

        def optionBtn_cb():
            dlg = dlgs.OptionsDialog(self.app)
            self.app.open(dlg)

        self.optionsBtn.connect(gui.CLICK, optionBtn_cb)

class AnimationEngine(template.AnimationEngineTemplate):
    def __init__(self, disp):
        super(AnimationEngine, self).__init__(disp)
        self.app = exp.Experiment(self.disp)
        self.app.engine = self
        self.rect = self.app.get_render_area()



    def setExperimentVariables(self):
        pass

    def genValues(self):
        return (0.344709897611) * self.currentTemp + 94.106

    def sendValues(self,pressure):
        self.app.tableArea.addToTable(pressure)


    def render(self, rect):
        self.disp.fill(colours.BLUE)    # Background Colour to complement menu colour


        return (rect,)  #Give back rect that has been drawn on
