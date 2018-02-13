from Experiments.RadioactiveDecay import experiment as exp
import resources.Colour as colours
from Experiments.RadioactiveDecay import dialogs as dlgs
from Experiments import ExperimentObjects as template
import externalModules.pgu.pgu.gui as gui
import math
import pygame
import Experiments.RadioactiveDecay.drawGraph as g
import resources.Equipment.RadioactivityEquipment as equipment
import resources.resourceManager as resM

pygame.font.init()
myFont = pygame.font.SysFont('Arial',20)

class TableArea(template.TableAreaTemplate):
    def __init__(self,width,height,app):
        super(TableArea, self).__init__(width,height,app)
        self.exponentialGraph = g.Graph("Time/s","No. of Undecayed Atoms","Exponential Decay",1)
        self.lnGraph = g.Graph("Time/s","ln(No. of Undecayed Atoms)","Natural Log of Undecayed Atoms",2)

        self.currentColumn = 1

    def setup(self):
        minIV = self.app.engine.startTime
        maxIV = self.app.engine.endTime
        interval = self.app.engine.timeInterval

        cellStyle = {'border':1}

        currentNum = minIV
        self.tr()
        self.td(gui.Label("Time/s"),style = cellStyle)
        while currentNum <= maxIV:
            self.exponentialGraph.xPoints.append(int(currentNum))
            self.lnGraph.xPoints.append(int(currentNum))
            lbl = gui.Label(str(currentNum))
            self.td(lbl,style = cellStyle)
            currentNum += interval

        self.tr()
        self.td(gui.Label("Number of Undecayed Atoms,N"),style = cellStyle)
        self.tr()
        self.td(gui.Label("ln(N)"),style = cellStyle)

    def addValuesToTable(self,undecayedAtoms):
        #Creates Label and adds it to its relevant Row
        undecayedAtomsLbl = gui.Label(str(round(undecayedAtoms,2)))
        self.td(undecayedAtomsLbl,col = self.currentColumn, row = 1, style= {'border':1})
        lnuA = gui.Label(str(round(math.log(undecayedAtoms),2)))
        self.td(lnuA,col = self.currentColumn, row = 2, style= {'border':1})
        self.exponentialGraph.yPoints.append(undecayedAtoms)
        self.lnGraph.yPoints.append(math.log(undecayedAtoms))
        self.currentColumn += 1

class MenuArea(template.MenuAreaTemplate):
    def __init__(self,width,height,app):
        super(MenuArea, self).__init__(width,height,app)
        self.variablesDlg = dlgs.VariablesDialog(["100","1000","100"])
        self.setupButtons()

    def setupButtons(self):
        self.graphBtn = template.createButton("Graph")

        self.variablesBtn = template.createButton("Input Variables")

        self.startExperimentBtn = template.createButton("Start Experiment")

        self.pauseExperimentBtn = template.createButton("Pause Experiment")

        self.restartExperimentBtn = template.createButton("Restart Experiment")

        self.instructionBtn = template.createButton("Instructions/Links")

        self.questionBtn = template.createButton("Questions")

        self.optionsBtn = template.createButton("Back To Menu")

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
            if (self.app.engine.isPaused):
                self.pauseExperimentBtn.value = "Play Experiment"
            else:
                self.pauseExperimentBtn.value = "Pause Experiment"

        self.pauseExperimentBtn.connect(gui.CLICK, pauseExperiment_cb)

        def restartExperimentBtn_cb():
            self.app.restart()

        self.restartExperimentBtn.connect(gui.CLICK, restartExperimentBtn_cb)

        def menuBtn_cb():
            import MainMenu as m
            m.run()

        self.optionsBtn.connect(gui.CLICK, menuBtn_cb)


        # Adding the buttons to the table
        self = template.addBtnToTbl(self, self.graphBtn)
        self = template.addBtnToTbl(self, self.variablesBtn)
        self = template.addBtnToTbl(self, self.startExperimentBtn)
        self = template.addBtnToTbl(self, self.pauseExperimentBtn)
        self = template.addBtnToTbl(self, self.restartExperimentBtn)
        self = template.addBtnToTbl(self, self.instructionBtn)
        self = template.addBtnToTbl(self, self.questionBtn)
        self = template.addBtnToTbl(self, self.optionsBtn)

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
                    self.app.engine.startTime = self.variablesDlg.startTime
                    self.app.engine.endTime = self.variablesDlg.endTime
                    self.app.engine.timeInterval = self.variablesDlg.timeInterval


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
        self.timeInterval = None

        self.container = equipment.Container(self.rect.left + 100,20,self.rect.right - 120,self.rect.bottom - 40)

        self.time = 0
        self.decayConstant = 0.0029957322737271

        self.startUndecayed = self.container.actualUndecayed
        self.actualUndecayed = self.container.actualUndecayed
        self.genExpected()

        atomsLabelImg = pygame.image.load(resM.atomLabels)
        self.atomsLabelImg = pygame.transform.scale(atomsLabelImg,(90,90))
        self.undecayedLbl = myFont.render("Undecayed",False,(0,0,0))
        self.decayedLbl = myFont.render("Decayed",False,(0,0,0))

    def sendValues(self,noOfUndecayedAtoms):
        self.app.tableArea.addValuesToTable(noOfUndecayedAtoms)

    def genExpected(self):
        x = self.startUndecayed * math.exp(-self.decayConstant * self.time)     #Calculate...
        self.calculatedUndecayed = round(x)                                     #Round as can't have float number of particles

    def setExperimentVariables(self):
        self.nextRecordPoint = self.startTime

    def render(self, rect):
        self.disp.fill(colours.BLUE)    # Background Colour to complement menu colour

        self.container.draw(self.disp)  #Draws Atoms

        #Labels to keep track of time and undecayed nuclei
        time = myFont.render("Time: "+str(self.time), False, (0, 0, 0))
        undecayedCount = myFont.render("N: "+str(self.actualUndecayed),False,(0,0,0))
        self.disp.blit(time, (10, 10))
        self.disp.blit(undecayedCount,(10,40))
        self.disp.blit(self.atomsLabelImg,(0,70))
        self.disp.blit(self.decayedLbl,(15,95))
        self.disp.blit(self.undecayedLbl,(10,140))

        if not self.isPaused:
            self.container.moveAtoms()

        if not self.isSetup and self.app.variablesInputted:
            self.setExperimentVariables()
            self.isSetup = True

        if not self.isPaused and self.app.animationRunning:

            if self.time == self.nextRecordPoint and not self.time > self.endTime:
                self.app.animationArea.save_background()
                self.sendValues(self.actualUndecayed)
                self.nextRecordPoint += self.timeInterval
            else:
                self.app.experimentFinished = True

            #Increase time then check how many should be decayed
            self.time += 1
            self.genExpected()

            #Gets the number of undecayed to the correct amount
            if self.actualUndecayed > self.calculatedUndecayed:
                self.container.decayAtoms(self.calculatedUndecayed)
                self.actualUndecayed = self.calculatedUndecayed #Updates actualUndecayed Value



            if self.time > 1000:   #Stops particles decaying after 1000s
                self.app.animationRunning = False


        return (rect,)  #Give back rect that has been drawn on
