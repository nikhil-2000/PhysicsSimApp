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
        #Get Variables
        cartWeights = self.app.engine.cartWeights
        massHolderWeights = self.app.engine.massHolderWeights
        weightSize = self.app.engine.weightSize

        cellStyle = {'border':1} #Sets border for each cell

        self.tr()
        self.td(gui.Label("Weight Force on Mass Holder/kg"),style = cellStyle)#First Table heading
        while cartWeights >= 0:
            #Adds each weight which the mass holder will have on it
            weightInKg = massHolderWeights * weightSize
            lbl = gui.Label(str(round(weightInKg,2)))
            self.td(lbl,style = cellStyle)
            #Shifts weight from cart to massHolder
            cartWeights -= 1
            massHolderWeights += 1

        #Renew Variables
        cartWeights = self.app.engine.cartWeights
        massHolderWeights = self.app.engine.massHolderWeights
        weightSize = self.app.engine.weightSize

        self.tr()
        self.td(gui.Label("Weight Force of Mass Holder/N"),style = cellStyle)#2nd Table Header
        while cartWeights >= 0:
            #Adds Weight Force for Mass Holder
            weightInN = massHolderWeights * weightSize * 9.81
            self.xPoints.append(weightInN)
            lbl = gui.Label(str(round(weightInN,3)))
            self.td(lbl,style = cellStyle)
            cartWeights -= 1
            massHolderWeights += 1

        #Adds columns for velocities and acceleration equation
        self.tr()
        self.td(gui.Label("Initial Velocity/(m/s)"),style = cellStyle)
        self.tr()
        self.td(gui.Label("Final Velocity/(m/s)"),style = cellStyle)
        self.tr()
        self.td(gui.Image(resM.accelerationEquation,height=48,width=84),style = cellStyle)

    def addValuesToTable(self,iVel,fVel,acc):
        #Creates Label and adds it to its relevant Row
        velLbl = gui.Label(str(round(iVel,2)))
        self.td(velLbl,col = self.currentColumn, row = 2, style= {'border':1})
        velLbl = gui.Label(str(round(fVel,2)))
        self.td(velLbl,col = self.currentColumn, row = 3, style= {'border':1})
        accLbl = gui.Label(str(round(acc,2)))
        #Sends Acceleration to Graph
        self.yPoints.append(acc)
        self.td(accLbl,col = self.currentColumn, row = 4, style= {'border':1})
        self.currentColumn += 1

class MenuArea(template.MenuAreaTemplate):
    def __init__(self,width,height,app):
        super(MenuArea, self).__init__(width,height,app)
        self.variablesDlg = dlgs.VariablesDialog(["100","6","1"])
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
                    self.app.engine.cartWeights = self.variablesDlg.cartWeights
                    self.app.engine.massHolderWeights = self.variablesDlg.massHolderWeights
                    self.app.engine.weightSize = self.variablesDlg.weightSize


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

        self.cartWeights = None
        self.massHolderWeights = None
        self.weightSize = None
        self.distanceBetweenGates = 1


        # Creating my Equipment
        self.bench = MEquip.Bench(self.disp,250)
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
        self.cart.noOfWeights = self.cartWeights
        self.massHolder.noOfWeights = self.massHolderWeights
        self.totalMass = (self.cartWeights + self.massHolderWeights) * self.weightSize
        self.recordedAtLG1 = False
        self.recordedAtLG2 = False


    def sendValues(self,acceleration,iVel,fVel):
        self.app.tableArea.addValuesToTable(iVel,fVel,acceleration)


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
            self.isSetup = True


        if not self.isPaused and self.app.animationRunning and self.cart.noOfWeights >= 0:

            speed = self.massHolder.getSpeed(self.massHolder.noOfWeights * self.weightSize * 9.81, self.totalMass)  # Fetches current speed
            pxSpeed = speed*10

            if not self.recordedAtLG1 and (self.cart.rect.centerx > self.LG1.rect.centerx):#As it passes LG1 centerx
                self.iVel = math.sqrt(2 * self.massHolder.acceleration * 1) #v^2 = u^2 + 2as where u = 0
                self.recordedAtLG1 = True
                # print("iVel")
                # print("Acc:",speed/self.massHolder.time)
                # print("time:",self.massHolder.time)
            elif not self.recordedAtLG2 and (self.cart.rect.right > self.LG2.rect.centerx):#As its about to pass LG2 centerx
                self.fVel = math.sqrt(2 * self.massHolder.acceleration * 2) #v^2 = u^2 + 2as where u = 0
                self.recordedAtLG2 = True
                self.app.animationArea.save_background()
                self.sendValues(speed/self.massHolder.time,self.iVel,self.fVel)
                # print("")
                # print("fVel")
                # print("Acc:",speed/self.massHolder.time)
                # print("time:",self.massHolder.time)


            if self.cart.rect.right + pxSpeed < self.pulley.left:  # If next shift is before pulley
                self.cart, self.massHolder = shift(self.cart, self.massHolder, pxSpeed)  # Move cart
            elif self.cart.rect.right == self.pulley.left:  # If cart is touching the pulley
                self.cart, self.massHolder = switchWeights(self.cart, self.massHolder)
                self.cart.rect.center = self.cart.startCenter
                self.massHolder.rect.center = self.massHolder.startCenter
                self.massHolder.time = 0
                self.recordedAtLG1 = False
                self.recordedAtLG2 = False
                pygame.time.delay(100)

            else:  # If the cart is about to hit the pulley
                self.cart.rect.right = self.pulley.left

            if self.cart.noOfWeights == 0:
                self.app.experimentFinished = True
                
                
        return (rect,)  #Give back rect that has been drawn on

def shift(cart,massHolder,speed):#Moves the cart by it's current speed
    cart.rect.x += speed
    massHolder.rect.y += speed
    return cart,massHolder

def switchWeights(cart,massHolder):#Takes a weight of the mass holder and moves it the cart
    massHolder.noOfWeights += 1
    cart.noOfWeights -= 1
    return cart,massHolder