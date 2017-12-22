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
                graphDlg = dlgs.GraphDialog(self.app)
                self.open(graphDlg)
            else:
                errorDlg = template.ErrorDlg("Finish the Experiment")
                self.app.open(errorDlg)


        self.graphBtn.connect(gui.CLICK,graph_cb)

        def variables_cb():
            self.variablesDlg.open()
            if self.variablesDlg.isValidated:
                #Updates the values of the Experiment Object
                self.app.variablesInputted = True
                self.app.minIV = self.variablesDlg.minIVValue
                self.app.maxIV = self.variablesDlg.maxIVValue
                self.app.interval = self.variablesDlg.intervalValue
                self.app.tableArea.setup()

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
        self.pressureGauge = pEquip.PressureGauge(self.beaker.rect.right - 42,self.rect.centery,30)
        self.thermometer = pEquip.Thermometer(self.beaker.rect.left + 55,self.rect.centery,300)


        self.equipment = pygame.sprite.Group()
        self.equipment.add(self.beaker)
        self.equipment.add(self.pressureGauge)
        self.equipment.add(self.thermometer)


        self.isSetup = False



    def setExperimentVariables(self):
        self.currentTemp = self.app.minIV
        self.finalTemp = self.app.maxIV
        self.intervalTemp = self.app.interval
        self.thermometer.setupMarker(self.disp,self.currentTemp)


    def genValues(self):

        current = exp.EMF / (self.currentResistance + exp.internalResistance)
        voltage = -current*exp.internalResistance + exp.EMF

        return current, voltage

    def sendValues(self,pressure):
        self.app.tableArea.addToTable(pressure)


    def render(self, rect):
            self.disp.fill(colours.BLUE)    # Background Colour to complement menu colour
            self.equipment.draw(self.disp)

            if not self.isSetup and self.app.variablesInputted:
                self.setExperimentVariables()

            if self.app.variablesInputted:
                self.thermometer.drawMarker(self.disp,self.currentTemp)

            if self.app.animationRunning and not (self.isPaused) and not (self.app.experimentFinished):
                pass


            return (rect,)  #Give back rect that has been drawn on


pygame.font.init()
LblFont = pygame.font.SysFont("Helvetica",20,True)
class DiagramLabel():
    def __init__(self,x,y,target,isVertical,isPositive,text):
        self.LblText = LblFont.render(text,True,colour.BLACK)   #Text for Label
        self.textRect = self.LblText.get_rect()
        self.textRect.center = x,y                              #Setting Label Position
        self.isVertical = isVertical                            #True(Up/Down) False(Left/Right)
        self.isPositive = isPositive                            #True(x/y-coordinate increasing) False(x/y-Coordinate Decreasing)
        self.target = target                                    #What is being labelled

    def draw(self,screen):
        screen.blit(self.LblText,self.textRect)     #Draw the Label
        lineWidth = 3
        #Setting the start points and end points of the line depending on the variables self.isVertical and self.isPositive
        if self.isVertical:
            if self.isPositive:
                startPoint = (self.textRect.center[0],self.textRect.bottom)
                endPoint = (self.target.rect.center[0],self.target.rect.top)
            else:
                startPoint = (self.textRect.center[0], self.textRect.top)
                endPoint = (self.target.rect.center[0], self.target.rect.bottom)
        else:
            if self.isPositive:
                startPoint = (self.textRect.left,self.textRect.center[1])
                endPoint = (self.target.rect.right,self.target.rect.center[1])
            else:
                startPoint = (self.textRect.right, self.textRect.center[1])
                endPoint = (self.target.rect.left, self.target.rect.center[1])

        pygame.draw.line(screen, colour.BLACK, startPoint, endPoint, lineWidth) #Draw the line from label to target

class DiagramLabel2():
    def __init__(self,x,y,target,isVertical,isPositive,text):
        self.LblText = LblFont.render(text,True,colour.BLACK)   #Text for Label
        self.textRect = self.LblText.get_rect()
        self.textRect.center = x,y                              #Setting Label Position
        self.isVertical = isVertical                            #True(Up/Down) False(Left/Right)
        self.isPositive = isPositive                            #True(x/y-coordinate increasing) False(x/y-Coordinate Decreasing)
        self.target = target                                    #What is being labelled

    def draw(self,screen):
        screen.blit(self.LblText,self.textRect)     #Draw the Label
        lineWidth = 3
        #Setting the start points and end points of the line depending on the variables self.isVertical and self.isPositive
        if self.isVertical:
            if self.isPositive:
                startPoint = (self.textRect.center[0],self.textRect.bottom)
                endPoint = (self.target.rect.center[0],self.target.top)
            else:
                startPoint = (self.textRect.center[0], self.textRect.top)
                endPoint = (self.target.center[0], self.target.bottom)
        else:
            if self.isPositive:
                startPoint = (self.textRect.left,self.textRect.center[1])
                endPoint = (self.target.right,self.target.center[1])
            else:
                startPoint = (self.textRect.right, self.textRect.center[1])
                endPoint = (self.target.left, self.target.center[1])

        pygame.draw.line(screen, colour.BLACK, startPoint, endPoint, lineWidth) #Draw the line from label to target



