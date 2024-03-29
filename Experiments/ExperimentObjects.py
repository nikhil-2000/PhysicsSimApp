import os
import sys
sys.path.append(os.path.abspath('..'))

# The previous lines were taken from https://stackoverflow.com/questions/10272879/how-do-i-import-a-python-script-from-a-sibling-directory
# It explained how to access modules in sibling directories

import pygame
from externalModules.pgu.pgu import gui, timer
import resources.Colour as colour

class ErrorDlg(gui.Dialog):
    def __init__(self, msg):
        gui.Dialog.__init__(self, gui.Label("ERROR"), gui.Label(msg))


class DrawingArea(gui.Widget):  # Same object as found in gui18.py in the pgu examples
    def __init__(self, width, height):
        gui.Widget.__init__(self, width=width, height=height)
        self.imageBuffer = pygame.Surface((width, height))

    def paint(self, surf):
        # Paint whatever has been captured in the buffer
        surf.blit(self.imageBuffer, (0, 0))

    # Call self function to take a snapshot of whatever has been rendered
    # onto the display over self widget.
    def save_background(self):
        disp = pygame.display.get_surface()
        self.imageBuffer.blit(disp, self.get_abs_rect())


class TableAreaTemplate(gui.Table):
    def __init__(self, width, height, app):
        gui.Table.__init__(self, width=width, height=height)
        self.app = app
        self.xPoints = []
        self.yPoints = []

    def setup(self):
        pass


# This will be run once the user has entered a valid set of variables

class MenuAreaTemplate(gui.Table):
    def __init__(self, width, height, app):
        gui.Table.__init__(self, width=width, height=height)
        self.app = app

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
                    errorDlg = ErrorDlg("Experiment is already running")
                    errorDlg.open()

            else:
                errorDlg = ErrorDlg("You haven't set the variables")
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

    def setup(self):
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
                    errorDlg = ErrorDlg("Experiment is already running")
                    errorDlg.open()

            else:
                errorDlg = ErrorDlg("You haven't set the variables")
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
            self.app.showLabels = not(self.app.showLabels)
            if self.app.showLabels:
                self.toggleLblsBtn.value = "Hide Labels"
            else:
                self.toggleLblsBtn.value = "Show Labels"

        self.toggleLblsBtn.connect(gui.CLICK, toggleLblsBtnBtn_cb)



        # Adding the buttons to the table
        self = addBtnToTbl(self, self.graphBtn)
        self = addBtnToTbl(self, self.variablesBtn)
        self = addBtnToTbl(self, self.startExperimentBtn)
        self = addBtnToTbl(self, self.pauseExperimentBtn)
        self = addBtnToTbl(self, self.toggleLblsBtn)
        self = addBtnToTbl(self, self.instructionBtn)
        self = addBtnToTbl(self, self.questionBtn)
        self = addBtnToTbl(self, self.optionsBtn)


class ExperimentTemplate(gui.Desktop):
    def __init__(self, screen):
        gui.Desktop.__init__(self)
        self.connect(gui.QUIT, self.quit)

        self.disp = screen
        self.engine = None
        self.animationAreaWidth = 650
        self.animationAreaHeight = 400
        self.animationArea = DrawingArea(self.animationAreaWidth, self.animationAreaHeight)

        self.menuArea = MenuAreaTemplate(screen.get_width() - self.animationAreaWidth, self.animationAreaHeight, self)

        self.tableArea = TableAreaTemplate(screen.get_width(), 200, self)

        self.variablesInputted = False
        self.animationRunning = False
        self.showLabels = False
        self.experimentFinished = False

        self.minIV = None
        self.maxIV = None
        self.interval = None

        topTbl = gui.Table()
        topTbl.tr()
        topTbl.td(self.animationArea)
        topTbl.td(self.menuArea)
        screenTbl = gui.Table(height=screen.get_height(), width=screen.get_width())

        screenTbl.tr()
        screenTbl.td(topTbl)
        screenTbl.tr()
        screenTbl.td(self.tableArea)

        self.menuArea.setup()

        self.init(screenTbl, screen)

    def open(self, dlg: object, pos: object = None) -> object:  # Same method as found in gui18.py in the pgu examples
        self.animationArea.save_background()  # Pause the gameplay while the dialog is visible
        running = not (self.engine.clock.paused)
        self.engine.clock.pause()
        gui.Desktop.open(self, dlg, pos)
        while (dlg.is_open()):
            for ev in pygame.event.get():
                self.event(ev)
            rects = self.update()
            if (rects):
                pygame.display.update(rects)
            if (running):
                self.engine.clock.resume()  # Resume gameplay

    def get_render_area(self):
        return self.animationArea.get_abs_rect()

    def restart(self):
        pass


class AnimationEngineTemplate(object):
    def __init__(self, disp):
        self.disp = disp
        self.app = ExperimentTemplate(self.disp)
        self.app.engine = self
        self.clock = timer.Clock()
        self.isPaused = False
        self.isSetup = False

    def render(self, rect):
        # Drawing code should go here

        return (rect,)

    def setupAnimation(self):
        # Called once the user has entered correct variables
        pass

    def run(self):  # This function is taken from the gui18.py which is in the pgu module under examples
        self.app.update(self.disp)
        pygame.display.flip()

        done = False

        while not done:
            for event in pygame.event.get():
                quitBool = (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
                if quitBool:
                    done = True
                else:
                    self.app.event(event)

            rect = self.app.get_render_area()
            updates = []
            self.disp.set_clip(rect)

            lst = self.render(rect)
            if (lst):
                updates += lst

            self.disp.set_clip()
            # Cap it at 30fps
            self.clock.tick(30)

            # Give pgu a chance to update the display
            lst = self.app.update(self.disp)
            if (lst):
                updates += lst
            pygame.display.update(updates)
            pygame.time.wait(10)

        pygame.quit()


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

class DiagramLabelPointToPoint():
    def __init__(self,lblPoint,targetPoint,isVertical,leftToRightorUpToDown,text):
        self.LblText = LblFont.render(text, True, colour.BLACK)  # Text for Label
        self.textRect = self.LblText.get_rect()
        self.textRect.center = lblPoint  # Setting Label Position
        self.isVertical = isVertical  # True(Up/Down) False(Left/Right)
        self.leftToRightorUpToDown = leftToRightorUpToDown


        self.targetPoint = targetPoint  # What is being labelled

    def draw(self, screen):
        screen.blit(self.LblText, self.textRect)  # Draw the Label
        lineWidth = 3
        # Setting the start points and end points of the line depending on the variables self.isVertical and self.isPositive
        if self.isVertical:
            if self.leftToRightorUpToDown:
                startPoint = self.textRect.centerx,self.textRect.bottom
            else:
                startPoint = self.textRect.centerx,self.textRect.top

        else:
            if self.leftToRightorUpToDown:
                startPoint = self.textRect.right,self.textRect.centery
            else:
                startPoint = self.textRect.left,self.textRect.centery

        pygame.draw.line(screen, colour.BLACK, startPoint, self.targetPoint, lineWidth)  # Draw the line from label to target

def createButton(text):
    return gui.Button(text, width=225, height=40)


def addBtnToTbl(tbl, btn):
    tbl.tr()
    tbl.td(btn)
    return tbl