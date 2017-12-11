import resources.resourceManager as resM
from Experiments.ResistivityOfAMetal.dialogs import *
from Experiments.ResistivityOfAMetal.experiment import *
import resources.Colour as colours

class Ball(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = pygame.image.load(resM.atomImg)
        self.image = pygame.transform.scale(self.image, (20, 20))

        self.rect = self.image.get_rect()

        self.rect.x = 10
        self.rect.y = 10
        self.xSpeed = -5
        self.ySpeed = -5
        self.ballsLeft = 5

    def changePlace(self):
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed

    def move(self,screenArea):

        self.rect.move_ip(self.xSpeed, self.ySpeed)
        if self.rect.right > screenArea.right or self.rect.left < screenArea.left:
            self.xSpeed *= -1

        if self.rect.top == screenArea.top or self.rect.bottom == screenArea.bottom:
            self.ySpeed *= -1


        self.rect.clamp_ip(screenArea)


class TableArea(template.TableAreaTemplate):
    def __init__(self,width,height,app):
        super(TableArea, self).__init__(width,height,app)
        self.xPoints = []
        self.yPoints = [1,2,3,4,5,6,7,8,9,10]

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


class MenuArea(template.MenuAreaTemplate):
    def __init__(self,width,height,app):
        super(MenuArea, self).__init__(width,height,app)
        self.variablesDlg = VariablesDialog(["10","100","10"], 0, 100)
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
                self.app.experimentFinished = True


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

        def constant_cb():
            constantsDlg = ConstantsDialog()
            self.open(constantsDlg)

        self.constantsBtn.connect(gui.CLICK,constant_cb)

        def instructions_cb():
            instructionsDlg = InstructionsLinkDialog()
            self.open(instructionsDlg)

        self.instructionBtn.connect(gui.CLICK,instructions_cb)

class AnimationEngine(template.AnimationEngineTemplate):
    def __init__(self, disp):
        super(AnimationEngine, self).__init__(disp)
        self.app = Experiment(self.disp)
        self.app.engine = self

        ballImg = pygame.image.load(resM.atomImg)
        self.ball = Ball()
        self.spriteGroup = pygame.sprite.Group()
        self.spriteGroup.add(self.ball)

    def render(self, dest, rect):

        dest.fill(colours.GREEN)
        self.spriteGroup.draw(dest)
        if self.app.animationRunning and not(self.isPaused):
            self.ball.move(rect)

        return (rect,)