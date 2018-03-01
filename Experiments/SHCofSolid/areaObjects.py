from Experiments.SHCofSolid import experiment as exp
import resources.Colour as colours
from Experiments.SHCofSolid import dialogs as dlgs
from Experiments import ExperimentObjects as template
import externalModules.pgu.pgu.gui as gui
import pygame
import resources.Equipment.SHCequipment as sEquip

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
        self.td(gui.Label("Time/s"),style = cellStyle)
        while currentNum <= maxIV:
            self.xPoints.append(int(currentNum))
            lbl = gui.Label(str(currentNum))
            self.td(lbl,style = cellStyle)
            currentNum += interval


        self.tr()
        self.td(gui.Label("Temperature/°C"),style = cellStyle)


    def addToTable(self,temperature):
        temperatureLbl = gui.Label(str(round(temperature,2)))                                           #Round the values to make
        self.app.tableArea.td(temperatureLbl, col=self.currentColumn, row=1, style={'border': 1})   #Adding the values
        self.yPoints.append(temperature)#Adds the unrounded values to y-points
        self.currentColumn += 1 # Increments columnCount for the add next value



class MenuArea(template.MenuAreaTemplate):
    def __init__(self,width,height,app):
        super(MenuArea, self).__init__(width,height,app)
        self.variablesDlg = dlgs.VariablesDialog(["50","500","50"])
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

        self.startTime = None
        self.endTime = None
        self.interval = None

        self.currentTime = 0
        self.nextRecordPoint = 0

        self.block = sEquip.CopperBlock(100, 100, 400, 300)
        self.block.insertThermometer()
        self.block.insertHeater()

        self.equipment = pygame.sprite.Group()
        self.equipment.add(self.block.thermometer)
        self.equipment.add(self.block.heater)
        self.block.thermometer.setupMarker(self.disp, 20)

        self.labels = []
        # self.labels.append()
        # self.labels.append()
        # self.labels.append()

    def setExperimentVariables(self):
        self.startTime = self.app.minIV
        self.currentTime = self.startTime
        self.nextRecordPoint = self.startTime
        self.endTime = self.app.maxIV
        self.interval = self.app.interval


    def genValues(self):
        return 20 + (exp.power * self.currentTime)/(exp.mass * exp.SHC)

    def sendValues(self,temperature):
        self.app.tableArea.addToTable(temperature)


    def render(self, rect):
            self.disp.fill(colours.BLUE)    # Background Colour to complement menu colour
            temperature = self.genValues()
            self.block.thermometer.drawMarker(self.disp, temperature)
            self.equipment.draw(self.disp)
            self.block.draw(self.disp)


            if not self.isSetup and self.app.variablesInputted:
                self.setExperimentVariables()
                self.isSetup = True

            if self.app.showLabels:
                for label in self.labels:
                    label.draw(self.disp)


            if self.app.animationRunning and not (self.isPaused) and not (self.app.experimentFinished):
                if self.currentTime == self.nextRecordPoint:
                    self.sendValues(temperature)
                    self.nextRecordPoint += self.interval

                if self.currentTime == self.endTime:
                    self.app.experimentFinished = True

                self.currentTime += 1

            return (rect,)  #Give back rect that has been drawn on





