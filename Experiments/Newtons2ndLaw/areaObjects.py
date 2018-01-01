from Experiments.Newtons2ndLaw import experiment as exp
import resources.Colour as colours
from Experiments.Newtons2ndLaw import dialogs as dlgs
from Experiments import ExperimentObjects as template
import externalModules.pgu.pgu.gui as gui
import resources.resourceManager as resM
import resources.Equipment.MotionEquipment as MEquip
import pygame
import math


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
        self.td(gui.Label("Weight Force of Mass Holder/N"),style = cellStyle)
        while currentNum <= maxIV:
            self.xPoints.append(round(currentNum*9.81,2))
            lbl = gui.Label(str(currentNum))
            self.td(lbl,style = cellStyle)
            currentNum += interval


        self.tr()
        self.td(gui.Label("Initial Velocity/(m/s)"),style = cellStyle)
        self.tr()
        self.td(gui.Label("Final Velocity/(m/s)"),style = cellStyle)
        self.tr()
        self.td(gui.Image(resM.accelerationEquation,height=48,width=84),style = cellStyle)


    def addToTable(self,pressure):
        pressureLbl = gui.Label(str(round(pressure,2)))                                          #Round the values to make
        self.app.tableArea.td(pressureLbl, col=self.currentColumn, row=1, style={'border': 1})   #Adding the values
        self.yPoints.append(pressure)#Adds the unrounded values to y-points
        self.currentColumn += 1 # Increments columnCount for the add next value

class MenuArea(template.MenuAreaTemplate):
    def __init__(self,width,height,app):
        super(MenuArea, self).__init__(width,height,app)
        self.variablesDlg = dlgs.VariablesDialog(["100","1000","100"])
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

        # Creating my Equipment
        self.bench = MEquip.Bench(self.disp,200)
        self.cart = MEquip.Cart(self.disp, self.bench)
        self.pulley = MEquip.Pulley(self.disp, self.bench)
        self.massHolder = MEquip.MassHolder(self.disp, self.pulley)
        self.LG1 = MEquip.LightGate(self.disp, self.bench, 1)
        self.LG2 = MEquip.LightGate(self.disp, self.bench, 2)

        # Adding all sprite objects to group
        self.equipment = pygame.sprite.Group()
        self.equipment.add(self.bench)
        self.equipment.add(self.cart)
        self.equipment.add(self.massHolder)
        self.equipment.add(self.LG1)
        self.equipment.add(self.LG2)

    def setExperimentVariables(self):
        self.massHolderStartWeight = int(self.app.minIV)
        self.massHolderEndWeight = int(self.app.maxIV)
        self.massInterval = int(self.app.interval)
        self.totalWeight =

    def genValues(self):
        return (0.344709897611) * self.currentTemp + 94.106

    def sendValues(self,pressure):
        self.app.tableArea.addToTable(pressure)


    def render(self, rect):
        self.disp.fill(colours.BLUE)    # Background Colour to complement menu colour

        pygame.draw.line(self.disp, colours.BLACK, (self.cart.rect.right, self.pulley.top), (self.pulley.x, self.pulley.top),
                         1)  # Connects string from cart to top pulley
        pygame.draw.arc(self.disp, colours.BLACK, [self.pulley.left, self.pulley.top, 2 * self.pulley.radius, 2 * self.pulley.radius], 0, math.pi / 2,
                        1)  # Wraps around pulley

        pygame.draw.line(self.disp, colours.BLACK, (self.pulley.right, self.pulley.y), (self.massHolder.rect.centerx, self.massHolder.rect.top),
                         1)  # Pulley to mass holder

        self.equipment.draw(self.disp)  # Draws Equipment
        self.pulley.draw()  # Draw Pulley
        self.massHolder.drawWeights()  # Draws Weights for massHolder
        self.cart.drawWeights()  # Draws Weights for Cart

        if not self.isSetup and self.app.variablesInputted:
            self.setExperimentVariables()


        if not self.isPaused and self.app.animationRunning:
            pass
            # speed = self.massHolder.getSpeed()  # Fetches current speed
            #
            # if self.cart.rect.right + speed < self.pulley.left:  # If next shift is before pulley
            #     cart, massHolder = shift(cart, massHolder, speed)  # Move cart
            # elif cart.rect.right == pulley.left:  # If cart is touching the pulley
            #     cart, massHolder = switchWeights(cart, massHolder)
            #     cart.rect.center = cart.startCenter
            #     massHolder.rect.center = massHolder.startCenter
            # else:  # If the cart is about to hit the pulley
            #     cart.rect.right = pulley.left
                
                
        return (rect,)  #Give back rect that has been drawn on
