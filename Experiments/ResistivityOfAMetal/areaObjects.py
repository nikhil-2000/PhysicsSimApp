import resources.resourceManager as resM
from Experiments.ResistivityOfAMetal.dialogs import *
from Experiments.ResistivityOfAMetal.experiment import *
import resources.Colour as colours
from resources.Equipment.ElectricalComponents import *
from Experiments.ResistivityOfAMetal import dialogs as dlgs


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
        self.td(gui.Label("Length of Wire/cm"),style = cellStyle)
        while currentNum <= maxIV:
            self.xPoints.append(int(currentNum))
            lbl = gui.Label(str(currentNum))
            self.td(lbl,style = cellStyle)
            currentNum += interval


        self.tr()
        self.td(gui.Label("Current"),style = cellStyle)
        self.tr()
        self.td(gui.Label("Resistance"),style = cellStyle)

    def addToTable(self,current,resistance):
        currentLbl = gui.Label(str(round(current,2)))                                           #Round the values to make
        resistanceLbl = gui.Label(str(round(resistance, 2)))                                    #them more presentable
        self.app.tableArea.td(currentLbl, col=self.currentColumn, row=1, style={'border': 1})   #Adding the values
        self.app.tableArea.td(resistanceLbl, col=self.currentColumn, row=2, style={'border': 1})#To the tables
        self.yPoints.append(resistance)#Adds the unrounded values to y-points
        self.currentColumn += 1 # Increments columnCount for the add next value


class MenuArea(template.MenuAreaTemplate):
    def __init__(self,width,height,app):
        super(MenuArea, self).__init__(width,height,app)
        self.variablesDlg = VariablesDialog(["10","100","10"])
        self.setupButtons()


    def setupButtons(self):
        self.setup()

        def graph_cb():
            if self.app.experimentFinished:
                xPoints = self.app.tableArea.xPoints
                yPoints = self.app.tableArea.yPoints
                graphDlg = GraphDialog(xPoints,yPoints)
                self.open(graphDlg)
            else:
                errorDlg = template.ErrorDlg("Finish the Experiment")
                self.app.open(errorDlg)


        self.graphBtn.connect(gui.CLICK,graph_cb)

        def variables_cb():
            self.variablesDlg.open()
            if self.variablesDlg.isValidated:
                #Updates the values of the Experiment Object
                self.app.variableInputted = True
                self.app.minIV = self.variablesDlg.minIVValue
                self.app.maxIV = self.variablesDlg.maxIVValue
                self.app.interval = self.variablesDlg.intervalValue

        self.variablesBtn.connect(gui.CLICK,variables_cb)

        def question_cb():
            qDlg = Questions(self.app)
            self.open(qDlg)

        self.questionBtn.connect(gui.CLICK,question_cb)

        def instructions_cb():
            instructionsDlg = InstructionsLinkDialog()
            self.open(instructionsDlg)

        self.instructionBtn.connect(gui.CLICK,instructions_cb)

        def optionBtn_cb():
            dlg = dlgs.OptionsDialog(self.app)
            self.app.open(dlg)

        self.optionsBtn.connect(gui.CLICK, optionBtn_cb)

class AnimationEngine(template.AnimationEngineTemplate):
    def __init__(self, disp):
        super(AnimationEngine, self).__init__(disp)
        self.app = Experiment(self.disp)
        self.app.engine = self
        self.components = pygame.sprite.Group()
        self.rect = self.app.get_render_area()

        self.circuitTop = 50
        self.circuitBottom = self.rect.bottom - 50
        self.circuitLeft = self.rect.left + 50
        self.circuitRight = self.rect.right - 50

        self.battery = Battery(self.rect.center[0], 50, 40, 40)
        self.ammeter = Ammeter(50, self.rect.center[1] // 2, 40)
        self.voltmeter = Voltmeter(self.rect.center[0], self.rect.center[1], 40)
        self.constantanWire = ConstantanWire(self.rect.center[0], self.circuitBottom, self.rect.width - 200, 3)
        self.crocSlideX = self.constantanWire.rect.left

        self.components.add(self.battery)
        self.components.add(self.ammeter)
        self.components.add(self.voltmeter)
        self.components.add(self.constantanWire)

        self.wireColour = list(colours.RED)

        voltmeterLabel = DiagramLabel(self.voltmeter.centerX,self.voltmeter.rect.top - 30,self.voltmeter,True,True,"Voltmeter")
        ammeterLabel = DiagramLabel(self.ammeter.rect.right + 70, self.ammeter.centerY,self.ammeter,False,True,"Ammeter")
        batteryLabel = DiagramLabel(self.battery.centerX,self.battery.rect.bottom+ 30,self.battery,True,False,"Battery")
        wireLabel = DiagramLabel(self.constantanWire.centerX,self.constantanWire.centerY+30,self.constantanWire,True,False,"Constantan Wire")
        self.labels = []
        self.labels.append(voltmeterLabel)
        self.labels.append(ammeterLabel)
        self.labels.append(batteryLabel)
        self.labels.append(wireLabel)

        self.endPointCalculated = False

    def setExperimentVariables(self):
        self.endingPoint = self.constantanWire.rect.left + ((self.app.maxIV/maxRange) * self.constantanWire.rect.width)
        self.currentLength = self.app.minIV


    def genValues(self):
        if self.currentLength == 0:
            return 0, 0

        resistance = (resistivity * self.currentLength)/ (100 * csa)
        current = voltage / resistance

        return current, resistance

    def sendValues(self,current,resistance):
        self.app.tableArea.addToTable(current,resistance)


    def render(self, rect):
            self.disp.fill(colours.BLUE)    # Background Colour to complement menu colour
            self.components.draw(self.disp) # Draws components initialised above

            points = []
            points.append((self.battery.rect.left,self.battery.centerY))#left battery
            points.append((self.ammeter.centerX, self.battery.centerY)) #topleft corner
            points.append((self.ammeter.centerX,self.ammeter.rect.top)) #top Ammeter
            pygame.draw.lines(self.disp,self.wireColour,False,points, 3)     #draw section

            points = []
            points.append((self.ammeter.centerX,self.ammeter.rect.bottom))  #bottom Ammeter
            points.append((self.ammeter.centerX,self.voltmeter.centerY))    #Middle left
            points.append((self.voltmeter.rect.left,self.voltmeter.centerY))#Left Voltmeter
            pygame.draw.lines(self.disp,self.wireColour,False,points,3)

            points = []
            points.append((self.voltmeter.rect.right,self.voltmeter.centerY))   #Right Voltmeter
            points.append((self.circuitRight ,self.voltmeter.centerY))          #Right Middle
            points.append((self.circuitRight ,self.battery.centerY))            # Top Right
            points.append((self.battery.rect.right,self.battery.centerY))       #Right Battery
            pygame.draw.lines(self.disp,self.wireColour,False,points,3)

            points = []
            points.append((self.circuitLeft,self.voltmeter.centerY))                    # Left Middle
            points.append((self.circuitLeft, self.circuitBottom))                       #Bottom Left
            points.append((self.constantanWire.rect.left, self.constantanWire.centerY)) #MainWireLeft
            pygame.draw.lines(self.disp,self.wireColour,False,points,3)


            movingCrocPoints = []
            basePoint = [self.crocSlideX, self.constantanWire.rect.top]     #Bottom of crocClip
            movingCrocPoints.append(basePoint)
            movingCrocPoints.append([basePoint[0] - 10,basePoint[1] - 30])  #Top Left of Croc Clip
            movingCrocPoints.append([basePoint[0] + 10,basePoint[1] - 30])  #Top Right of Croc Clip
            pygame.draw.polygon(self.disp,self.wireColour,movingCrocPoints,0)

            points = []
            #Connecting from Croc Clip to rest of circuit
            points.append((basePoint[0],basePoint[1] - 30))
            points.append((basePoint[0],basePoint[1] - 80))
            points.append((self.circuitRight,basePoint[1] - 80))
            points.append((self.circuitRight,self.voltmeter.centerY))
            pygame.draw.lines(self.disp,self.wireColour,False,points,3)

            if self.app.showLabels:         #If the user wants to see the labels
                for label in self.labels:
                    label.draw(self.disp)   #Draw them onto the screen


            if self.app.animationRunning and not(self.isPaused) and not(self.app.experimentFinished):
                if not (self.endPointCalculated):
                    #Sets up the experiment if it hasn't happened yet
                    self.setExperimentVariables()
                    self.endPointCalculated = True

                #Calculates where on the wire the next recording should be taken
                nextRecordPoint = self.constantanWire.rect.left + (self.constantanWire.rect.width * (self.currentLength)// maxRange)
                if self.crocSlideX == nextRecordPoint:      #If on recording point
                    self.app.animationArea.save_background()
                    current, resistance = self.genValues()  #Get values for current and resistance
                    self.sendValues(current, resistance)    #Add values to table and graph
                    self.currentLength += self.app.interval #Increment to the next length to be recorded at

                if self.crocSlideX < self.endingPoint:     #If it hasn't hit the end point
                    self.crocSlideX += 1                    #Slide Croc Clip by one each time
                else:                                       #Otherwise
                    self.app.experimentFinished = True      #End experiment


                if self.wireColour[1] == 155:
                    self.colourDirection = -5
                elif self.wireColour[1] == 0:
                    self.colourDirection = 5

                self.wireColour[1] += self.colourDirection


            return (rect,)  #Give back are that has been drawn on


pygame.font.init()
LblFont = pygame.font.SysFont("Helvetica",20,True)
class DiagramLabel():
    def __init__(self,x,y,target:pygame.sprite.Sprite,isVertical,isPositive,text):
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



