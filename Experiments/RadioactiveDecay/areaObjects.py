from Experiments.RadioactiveDecay import experiment as exp
import resources.Colour as colours
from Experiments.RadioactiveDecay import dialogs as dlgs
from Experiments import ExperimentObjects as template
import externalModules.pgu.pgu.gui as gui
import math
import Experiments.RadioactiveDecay.drawGraph as g
import resources.Equipment.RadioactivityEquipment as equipment


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
        self.td(undecayedAtomsLbl,col = self.currentColumn, row = 2, style= {'border':1})
        lnuA = gui.Label(str(round(math.log(undecayedAtoms),2)))
        self.td(lnuA,col = self.currentColumn, row = 3, style= {'border':1})
        self.exponentialGraph.yPoints.append(undecayedAtoms)
        self.lnGraph.yPoints.append(math.log(undecayedAtoms))
        self.currentColumn += 1

class MenuArea(template.MenuAreaTemplate):
    def __init__(self,width,height,app):
        super(MenuArea, self).__init__(width,height,app)
        self.variablesDlg = dlgs.VariablesDialog(["0","450","50"])
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



    def sendValues(self,noOfUndecayedAtoms):
        self.app.tableArea.addValuesToTable(noOfUndecayedAtoms)


    def render(self, rect):
        self.disp.fill(colours.BLUE)    # Background Colour to complement menu colour

        self.container.draw(self.disp)

        if not self.isSetup and self.app.variablesInputted:

            self.isSetup = True


        if not self.isPaused and self.app.animationRunning:

            pass
                
                
        return (rect,)  #Give back rect that has been drawn on

