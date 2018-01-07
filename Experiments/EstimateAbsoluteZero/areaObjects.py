from Experiments.EstimateAbsoluteZero import experiment as exp
import resources.Colour as colours
from resources.Equipment.ElectricalComponents import *
from Experiments.EstimateAbsoluteZero import dialogs as dlgs
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

        self.beaker = pEquip.WaterBeaker(self.rect.centerx,self.rect.centery,self.rect.height - 50)
        self.pressureGauge = pEquip.PressureGauge(self.beaker.rect.right - 63,self.rect.centery,50)
        self.thermometer = pEquip.Thermometer(self.beaker.rect.left + 55,self.rect.centery,300)
        self.bulbBeaker = pEquip.BulbBeaker(self.thermometer.minTemp,self.thermometer.maxTemp)


        self.equipment = pygame.sprite.Group()
        self.equipment.add(self.beaker)
        self.equipment.add(self.pressureGauge)
        self.equipment.add(self.thermometer)



        self.currentTemp = 20
        self.pressure = self.genValues()  # Get values for pressure

        self.thermometer.setupMarker(self.disp,self.currentTemp)
        self.pressureGauge.setupPointer(self.genValues(),self.disp)


        self.isSetup = False
        self.endTempCalculated = False

        thermometerLbl = template.DiagramLabel(self.thermometer.rect.left - 70, self.thermometer.rect.centery,self.thermometer,False,False,"Thermometer")
        pressureGaugeLbl = template.DiagramLabel(self.pressureGauge.rect.centerx, self.pressureGauge.rect.bottom + 60,self.pressureGauge,True,False,"Pressure Gauge")
        bulbBeakerLbl = template.DiagramLabel(self.bulbBeaker.rect.centerx, self.bulbBeaker.rect.bottom + 40,self.bulbBeaker,True,False,"Bulb Beaker")

        self.labels = []
        self.labels.append(thermometerLbl)
        self.labels.append(pressureGaugeLbl)
        self.labels.append(bulbBeakerLbl)

    def setExperimentVariables(self):
        self.currentTemp = self.app.minIV
        self.pressure = self.genValues()
        self.nextRecordTemp = self.app.minIV
        self.finalTemp = self.app.maxIV
        self.intervalTemp = self.app.interval
        self.nextRecordTemp = self.app.minIV + self.intervalTemp
        self.thermometer.setupMarker(self.disp,self.currentTemp)
        self.currentIndex = 0

    def genValues(self):
        return (0.344709897611) * self.currentTemp + 94.106

    def sendValues(self,pressure):
        self.app.tableArea.addToTable(pressure)


    def render(self, rect):
            self.disp.fill(colours.BLUE)    # Background Colour to complement menu colour
            self.equipment.draw(self.disp)

            if not self.isPaused:
                self.bulbBeaker.moveAtoms(self.currentTemp)

            self.bulbBeaker.drawAtoms(self.disp)


            if not self.isSetup and self.app.variablesInputted:
                self.setExperimentVariables()
                self.isSetup = True

            if self.app.showLabels:
                for label in self.labels:
                    label.draw(self.disp)


            if self.app.animationRunning and not (self.isPaused) and not (self.app.experimentFinished):
                self.pressure = self.genValues()  # Get values for pressure
                if not (self.endTempCalculated):
                    # Sets up the experiment if it hasn't happened yet
                    self.setExperimentVariables()
                    self.endTempCalculated = True


                # Calculates where on the wire the next recording should be taken
                nextRecordPoint = self.app.tableArea.xPoints[self.currentIndex]
                if self.currentTemp == nextRecordPoint:  # If on recording point
                    self.app.animationArea.save_background()
                    self.sendValues(self.pressure)  # Add values to table and graph
                    if self.currentTemp != self.finalTemp:
                        self.currentIndex += 1

                if self.currentTemp <= self.finalTemp:
                    self.currentTemp = round(self.currentTemp + 0.2,1)
                else:
                    self.app.experimentFinished = True


            self.thermometer.drawMarker(self.disp,self.currentTemp)
            self.pressureGauge.drawPointer(self.disp,self.pressure)

            return (rect,)  #Give back rect that has been drawn on





