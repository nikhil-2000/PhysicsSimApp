

from Experiments.InternalResistance import experiment as exp
import resources.Colour as colours
from resources.Equipment.ElectricalComponents import *
from Experiments.InternalResistance import dialogs as dlgs
from Experiments.InternalResistance import drawGraph as g
from Experiments import ExperimentObjects as template
import externalModules.pgu.pgu.gui as gui




class TableArea(template.TableAreaTemplate):
    def __init__(self,width,height,app):
        super(TableArea, self).__init__(width,height,app)
        self.voltageCurrentGraph = g.Graph("Current/A","Voltage/V","Voltage-Current",1)
        self.resistanceCurrentGraph = g.Graph("1/(Current/A)","Resistance/Ω","Resistance-Current",2)

        self.currentColumn = 1

    def setup(self):
        minIV = self.app.minIV
        maxIV = self.app.maxIV
        interval = self.app.interval

        cellStyle = {'border':1}

        currentNum = minIV
        self.tr()
        self.td(gui.Label("Resistance/Ω"),style = cellStyle)
        while currentNum <= maxIV:
            self.resistanceCurrentGraph.yPoints.append(int(currentNum))
            lbl = gui.Label(str(currentNum))
            self.td(lbl,style = cellStyle)
            currentNum += interval

        self.tr()
        self.td(gui.Label("Current"),style = cellStyle)
        self.tr()
        self.td(gui.Label("Voltage"),style = cellStyle)


    def addToTable(self,current,voltage):
        currentLbl = gui.Label(str(round(current,3)))       #Round the values to make
        voltageLbl = gui.Label(str(round(voltage,2)))

        self.td(currentLbl, col=self.currentColumn, row=1, style={'border': 1})#Adding the values
        self.td(voltageLbl, col=self.currentColumn, row=2, style={'border': 1})   #To the tables

        self.voltageCurrentGraph.xPoints.append(current)
        self.voltageCurrentGraph.yPoints.append(voltage)
        if current != 0:
            self.resistanceCurrentGraph.xPoints.append(1/current)
        else:
            self.resistanceCurrentGraph.xPoints.append(0)

        self.currentColumn += 1 # Increments columnCount for the add next value


class MenuArea(template.MenuAreaTemplate):
    def __init__(self,width,height,app):
        super(MenuArea, self).__init__(width,height,app)
        self.variablesDlg = dlgs.VariablesDialog(["10","100","10"])
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
        self.components = pygame.sprite.Group()
        self.resistors = []

        self.circuitTop = 50
        self.circuitBottom = self.rect.bottom - 50
        self.circuitLeft = self.rect.left + 50
        self.circuitRight = self.rect.right - 50

        self.battery = Battery(self.rect.center[0], self.circuitTop, 40, 40)
        self.batteryResistor = Resistor(self.battery.rect.right + 30, self.circuitTop,30,10)
        self.ammeter = Ammeter(self.circuitLeft, self.rect.center[1], 40)
        factor = 8
        self.vResistor = vResistor(self.rect.centerx,self.circuitBottom,200,50)
        self.batRect = pygame.Rect((self.battery.rect.left - 10, self.battery.rect.top - 10), (120, 60))

        self.crocSlideX = self.vResistor.rect.left

        self.components.add(self.battery)
        self.components.add(self.ammeter)
        #self.components.add(self.vResistor)

        self.resistors.append(self.batteryResistor)
        self.resistors.append(self.vResistor)

        self.wireColour = list(colours.RED)

        ammeterLabel = DiagramLabel(self.ammeter.rect.right + 70, self.ammeter.centerY,self.ammeter,False,True,"Ammeter")
        batteryLabel = DiagramLabel2(self.batRect.centerx,self.batRect.bottom+ 30,self.batRect,True,False,"Battery")
        vResistorLabel = DiagramLabel(self.vResistor.rect.right + 100,self.vResistor.rect.centery,self.vResistor,False,True,"Variable Resistor")
        self.labels = []
        self.labels.append(ammeterLabel)
        self.labels.append(batteryLabel)
        self.labels.append(vResistorLabel)

        self.endPointCalculated = False

    def setExperimentVariables(self):
        self.endingPoint = self.vResistor.rect.left + ((self.app.maxIV/exp.maxRange) * self.vResistor.rect.width)
        self.currentResistance = self.app.minIV


    def genValues(self):

        current = exp.EMF / (self.currentResistance + exp.internalResistance)
        voltage = -current*exp.internalResistance + exp.EMF

        return current, voltage

    def sendValues(self,current,voltage):
        self.app.tableArea.addToTable(current,voltage)


    def render(self, rect):
            self.disp.fill(colours.BLUE)    # Background Colour to complement menu colour

            self.components.draw(self.disp)
            for res in self.resistors:
               res.draw(self.disp)

            if self.app.showLabels:
                for label in self.labels:
                    label.draw(self.disp)

            #Drawing wires
            points = []
            points.append((self.battery.rect.left,self.circuitTop))
            points.append((self.circuitLeft,self.circuitTop))
            points.append((self.circuitLeft,self.ammeter.rect.top))
            pygame.draw.lines(self.disp,self.wireColour,False,points,3)

            points = []
            points.append((self.circuitLeft,self.ammeter.rect.bottom))
            points.append((self.circuitLeft,self.circuitBottom))
            points.append((self.vResistor.rect.left,self.circuitBottom))
            pygame.draw.lines(self.disp,self.wireColour,False,points,3)


            fPoint = (self.battery.rect.right,self.battery.centerY)
            lPoint = (self.batteryResistor.rect.left,self.batteryResistor.centerY)
            pygame.draw.line(self.disp,self.wireColour,fPoint,lPoint,3)

            movingCrocPoints = []
            basePoint = [self.crocSlideX, self.vResistor.rect.top]     #Bottom of crocClip
            movingCrocPoints.append(basePoint)
            movingCrocPoints.append([basePoint[0] - 10,basePoint[1] - 30])  #Top Left of Croc Clip
            movingCrocPoints.append([basePoint[0] + 10,basePoint[1] - 30])  #Top Right of Croc Clip
            pygame.draw.polygon(self.disp,self.wireColour,movingCrocPoints,0)

            points = []
            #Connecting from Croc Clip to rest of circuit
            points.append((basePoint[0],basePoint[1] - 30))
            points.append((basePoint[0],basePoint[1] - 80))
            points.append((self.circuitRight,basePoint[1] - 80))
            points.append((self.circuitRight,self.circuitTop))
            points.append((self.batteryResistor.rect.right,self.circuitTop))
            pygame.draw.lines(self.disp,self.wireColour,False,points,3)

            pygame.draw.rect(self.disp,colour.BLACK,self.batRect, 1)

            if self.app.animationRunning and not (self.isPaused) and not (self.app.experimentFinished):
                if not (self.endPointCalculated):
                    # Sets up the experiment if it hasn't happened yet
                    self.setExperimentVariables()
                    self.endPointCalculated = True

                # Calculates where on the wire the next recording should be taken
                nextRecordPoint = self.vResistor.rect.left + (
                        self.vResistor.rect.width * (self.currentResistance) // exp.maxRange)
                if self.crocSlideX == nextRecordPoint:  # If on recording point
                    self.app.animationArea.save_background()
                    current, resistance = self.genValues()  # Get values for current and resistance
                    self.sendValues(current, resistance)  # Add values to table and graph
                    self.currentResistance += self.app.interval  # Increment to the next length to be recorded at

                if self.crocSlideX < self.endingPoint:  # If it hasn't hit the end point
                    self.crocSlideX += 1  # Slide Croc Clip by one each time
                else:  # Otherwise
                    self.app.experimentFinished = True  # End experiment


                if self.wireColour[1] == 155:
                    self.colourDirection = -5
                elif self.wireColour[1] == 0:
                    self.colourDirection = 5

                self.wireColour[1] += self.colourDirection



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



