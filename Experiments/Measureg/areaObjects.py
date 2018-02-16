from Experiments.Measureg import experiment as exp
import resources.Colour as colours
from Experiments.Measureg import dialogs as dlgs
from Experiments import ExperimentObjects as template
import externalModules.pgu.pgu.gui as gui
import resources.resourceManager as resM
import resources.Equipment.MotionEquipment as MEquip
import pygame
import math


class TableArea(template.TableAreaTemplate):
    def __init__(self, width, height, app):
        super(TableArea, self).__init__(width, height, app)
        # Points on the graph
        self.xPoints = []
        self.yPoints = []
        # Will be incremented after each addition to the table
        self.currentColumn = 1

    def setup(self):
        # Get Variables
        minIV = self.app.engine.startHeight
        maxIV = self.app.engine.endHeight
        interval = self.app.engine.heightInterval

        # Standardises the cell style
        cellStyle = {'border': 1}

        currentNum = minIV
        self.tr()  # New Row
        self.td(gui.Label("Height/m"), style=cellStyle)  # Add Row Heading
        while currentNum <= maxIV:  # Keep going till maxIV is in the table
            self.xPoints.append(currentNum/100)  # Adds to x points
            lbl = gui.Label(str(currentNum))  # Creates Labels
            self.td(lbl, style=cellStyle)
            currentNum += interval

        self.tr()
        self.td(gui.Label("Time,s"), style=cellStyle)  # Adds row heading for measured variable
        self.tr()
        self.td(gui.Label("Time²/s²"), style=cellStyle)  # Adds row heading for calculated variable

    def addValuesToTable(self, time):
        # Creates Label and adds it to its relevant Row
        timeLbl = gui.Label(str(round(time, 2)))
        self.td(timeLbl, col=self.currentColumn, row=1, style={'border': 1})
        timeLbl = gui.Label(str(round(time ** 2, 2)))
        self.td(timeLbl, col=self.currentColumn, row=2, style={'border': 1})
        self.yPoints.append(time ** 2)
        self.currentColumn += 1


class MenuArea(template.MenuAreaTemplate):
    def __init__(self, width, height, app):
        super(MenuArea, self).__init__(width, height, app)
        self.variablesDlg = dlgs.VariablesDialog(["20", "200", "20"])
        self.setupButtons()

    def createButtons(self):
        # All the buttons are created and organised here

        # The button variables are all created here
        self.graphBtn = createButton("Graph")

        self.variablesBtn = createButton("Input Variables")

        self.startExperimentBtn = createButton("Start Experiment")

        self.pauseExperimentBtn = createButton("Pause Experiment")

        self.toggleLblsBtn = createButton("Show Labels")

        self.instructionBtn = createButton("Instructions/Links")

        self.questionBtn = createButton("Questions")

        self.optionsBtn = createButton("Options")

        # The buttons' function are defined here

        def startExperiment_cb():
            if self.variablesDlg.isValidated:  # If the user inputs are valid
                if not (self.app.animationRunning):  # And if the animation hasn't started yet
                    self.app.animationRunning = True  # Tell the rest of the program that the animation can now run
                else:
                    errorDlg = template.ErrorDlg("Experiment is already running")
                    errorDlg.open()

            else:
                errorDlg = template.ErrorDlg("You haven't set the variables")
                errorDlg.open()

        self.startExperimentBtn.connect(gui.CLICK, startExperiment_cb)

        def pauseExperiment_cb():
            self.app.animationArea.save_background()
            self.app.engine.isPaused = not (self.app.engine.isPaused)
            if (self.app.engine.isPaused):
                self.pauseExperimentBtn.value = "Play Experiment"
            else:
                self.pauseExperimentBtn.value = "Pause Experiment"

        self.pauseExperimentBtn.connect(gui.CLICK, pauseExperiment_cb)

        def toggleLblsBtnBtn_cb():
            self.app.animationArea.save_background()
            self.app.showLabels = not (self.app.showLabels)
            if self.app.showLabels:
                self.toggleLblsBtn.value = "Hide Labels"
            else:
                self.toggleLblsBtn.value = "Show Labels"

        self.toggleLblsBtn.connect(gui.CLICK, toggleLblsBtnBtn_cb)

    def setupButtons(self):
        self.createButtons()

        def graph_cb():
            if self.app.experimentFinished:
                graphDlg = dlgs.GraphDialog(self.app.tableArea)
                self.open(graphDlg)
            else:
                errorDlg = template.ErrorDlg("Finish the Experiment")
                self.app.open(errorDlg)

        self.graphBtn.connect(gui.CLICK, graph_cb)

        def variables_cb():
            if not self.app.variablesInputted:
                self.variablesDlg.open()
                if self.variablesDlg.isValidated:
                    # Updates the values of the Experiment Object
                    self.app.variablesInputted = True
                    self.app.engine.startHeight = self.variablesDlg.startHeight
                    self.app.engine.endHeight = self.variablesDlg.endHeight
                    self.app.engine.heightInterval = self.variablesDlg.heightInterval

                    self.app.tableArea.setup()
            else:
                self.app.open(template.ErrorDlg("You have already inputted variables."))

        self.variablesBtn.connect(gui.CLICK, variables_cb)

        def question():
            questions = dlgs.Questions(self.app)
            self.open(questions)

        self.questionBtn.connect(gui.CLICK, question)

        def instructions_cb():
            instructionsDlg = dlgs.InstructionsLinkDialog()
            self.open(instructionsDlg)

        self.instructionBtn.connect(gui.CLICK, instructions_cb)

        def optionBtn_cb():
            dlg = dlgs.OptionsDialog(self.app)
            self.app.open(dlg)

        self.optionsBtn.connect(gui.CLICK, optionBtn_cb)

        addBtnsToRow(self,self.graphBtn,self.variablesBtn)
        addBtnsToRow(self,self.startExperimentBtn,self.pauseExperimentBtn)
        addBtnsToRow(self,self.questionBtn,self.instructionBtn)
        addBtnsToRow(self,self.toggleLblsBtn,self.optionsBtn)



class AnimationEngine(template.AnimationEngineTemplate):
    def __init__(self, disp):
        super(AnimationEngine, self).__init__(disp)
        self.app = exp.Experiment(self.disp)
        self.app.engine = self
        self.rect = self.app.get_render_area()

        self.startHeight = None
        self.endHeight = None
        self.heightInterval = None
        self.currentHeight = None


        self.runStarted = True

        self.equipment = pygame.sprite.Group()

        self.ruler = MEquip.Ruler(110, 5, 380)
        self.ball = MEquip.Ball(100, 375,20)
        self.clampStand = MEquip.ClampStand(115,0,400)

        self.equipment.add(self.ruler)
        self.equipment.add(self.ball)
        self.equipment.add(self.clampStand)

        self.rulerLabel = template.DiagramLabelPointToPoint((325,30),(self.ruler.rect.right,30),False,False,"Ruler")
        self.clampLabel = template.DiagramLabelPointToPoint((325,100),(250,100),False,False,"Clamp Stand")

    def setExperimentVariables(self):
        self.currentHeight = self.startHeight
        self.setBall()

    def sendValues(self, time):
        self.app.tableArea.addValuesToTable(time)

    def setBall(self):
        self.ball.rect.bottom = self.ruler.getStartPositionY(self.currentHeight,self.ruler.rect.bottom)
        print("Ball Bottom:", self.ball.rect.bottom)
        print("Ruler Top:", self.ruler.rect.top)
        self.ball.speed = 0
        self.time = 0

    def getTime(self):
        return math.sqrt(self.currentHeight*2/981)

    def render(self, rect):
        self.disp.fill(colours.BLUE)  # Background Colour to complement menu colour

        self.equipment.draw(self.disp)

        if self.app.showLabels:
            ballLabel = template.DiagramLabel(self.ball.rect.left - 40, self.ball.rect.centery, self.ball, False, False,
                                              "Ball")
            self.rulerLabel.draw(self.disp)
            self.clampLabel.draw(self.disp)
            ballLabel.draw(self.disp)

        if not self.isSetup and self.app.variablesInputted:
            self.setExperimentVariables()
            self.isSetup = True

        if not self.isPaused and self.app.animationRunning and not self.app.experimentFinished:
            if not self.runStarted:
                if self.currentHeight < self.endHeight: #Until currentHeight == endHeight
                    self.currentHeight += self.heightInterval
                    self.setBall()  #        self.ball.rect.bottom = self.ruler.getStartPositionY(self.currentHeight,400)
                    self.runStarted = True
                elif self.currentHeight == self.endHeight:#Last Iteration of
                    self.setBall()
                    print("Ball Bottom:",self.ball.rect.bottom)
                    print("Ruler Top:",self.ruler.rect.top)
                    self.runStarted = True

            else:
                self.ball.setSpeed(self.time)
                if self.ball.rect.bottom < self.ruler.rect.bottom:
                    self.ball.move()
                else:
                    self.ball.rect.bottom = self.ruler.rect.bottom
                    self.runStarted = False
                    self.sendValues(self.getTime())
                    pygame.time.wait(100)



            if self.currentHeight == self.endHeight and self.ball.rect.bottom == self.ruler.rect.bottom:
                self.app.experimentFinished = True


            self.time += 1/2
        return rect,  # Give back rect that has been drawn on



def addBtnsToRow(tbl, btn,btn2):
    tbl.tr()
    tbl.td(btn)
    tbl.td(btn2)

def createButton(text):
    return gui.Button(text, width=225, height=75)
