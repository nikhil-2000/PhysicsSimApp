
# self is not needed if you have PGU installed
import sys
import os
sys.path.append(os.path.abspath('..'))

#The previous lines were taken from https://stackoverflow.com/questions/10272879/how-do-i-import-a-python-script-from-a-sibling-directory
#It explained how to access modules in sibling directories

import math
import time
import pygame
import matplotlib.pyplot as plt

from externalModules.pgu.pgu import gui, timer

from resources.Colour import *
import resources.resourceManager as resM



class DrawingArea(gui.Widget):#Object for where the pygame animation will happen
    def __init__(self, width, height):
        gui.Widget.__init__(self, width=width, height=height)
        self.imageBuffer = pygame.Surface((width, height))

    def paint(self, surf):
        # Paint whatever has been captured in the buffer
        surf.blit(self.imageBuffer, (0, 0))

    # Call self function to take a snapshot of whatever has been rendered
    # onto the display over self widget.
    def save_background(self,blit):
        disp = pygame.display.get_surface()
        if blit:
            self.imageBuffer.blit(disp, self.get_abs_rect())
    

class InputDlg(gui.Dialog):# The dialog for variables to be inputted
    def __init__(self):
        title = gui.Label("Variables")
        main = gui.Table()
        print(main)
        self.minVar = None
        self.maxVar = None
        self.interval = None
        self.varsInputted = False
        
        MinLbl = gui.Label("Minimum Length")
        MinInp = gui.Input("")
        MaxLbl = gui.Label("Maximum Length")
        MaxInp = gui.Input("")
        IntervalLbl = gui.Label("Interval")
        IntervalInp = gui.Input("")

        def done_cb():#Validates user input
            minVar = MinInp.value
            maxVar = MaxInp.value
            interval = IntervalInp.value
            self.varsInputted,self.minVar,self.maxVar,self.interval,errorMsg = validateRange(minVar,maxVar,interval)
            if not(self.varsInputted):
                errorDlg = ErrorDlg(errorMsg)
                errorDlg.open()
                MinInp.value = ""
                MaxInp.value = ""
                IntervalInp.value = ""
            else:
                self.close()
            
        done = gui.Button("Done")
        done.connect(gui.CLICK, done_cb)

        def default_cb():
            MinInp.value = 10
            MaxInp.value = 100
            IntervalInp.value = 10
            
        default = gui.Button("Default Values")
        default.connect(gui.CLICK, default_cb)

        inputsTbl = gui.Table()
        inputsTbl.tr()
        inputsTbl.td(MinLbl)
        inputsTbl.td(MinInp)
        inputsTbl.td(gui.Label("cm"))
        inputsTbl.tr()
        inputsTbl.td(MaxLbl)
        inputsTbl.td(MaxInp)
        inputsTbl.td(gui.Label("cm"))
        inputsTbl.tr()
        inputsTbl.td(IntervalLbl)
        inputsTbl.td(IntervalInp)
        inputsTbl.td(gui.Label("cm"))
        

        btnsTbl = gui.Table()
        btnsTbl.tr()
        btnsTbl.td(done,style = {'padding':10})
        btnsTbl.td(default,style = {'padding':10})

        main.tr()
        main.td(gui.Label("The numbers you choose will be rounded up to the nearest ten"))
        main.tr()
        main.td(gui.Label("Choose two numbers between 0 and 100"))

        main.tr()
        main.td(inputsTbl)
        main.tr()
        main.td(btnsTbl)
        
        gui.Dialog.__init__(self,title,main)

class ErrorDlg(gui.Dialog):
    def __init__(self,msg):
        gui.Dialog.__init__(self,gui.Label("ERROR"),gui.Label(msg))

class ConstantsDlg(gui.Dialog):
    def __init__(self):
        
        constantsLbl = gui.Label("Constants")
        batteryVoltageLbl = gui.Label("Battery Voltage = 1.5 Volts")
        wireAreaLbl = gui.Label("Wire Cross Sectional Area = 0.00785 cm²")
        wireTypeLbl = gui.Label("Wire Type = Nichrome")

        tbl = gui.Table()

        lblStyle = {'padding':5}
        
        tbl.tr()
        tbl.td(constantsLbl,style = lblStyle)
        tbl.tr()
        tbl.td(batteryVoltageLbl,style = lblStyle)
        tbl.tr()
        tbl.td(wireAreaLbl,style = lblStyle)
        tbl.tr()
        tbl.td(wireTypeLbl,style = lblStyle)

        gui.Dialog.__init__(self,gui.Label("CONSTANTS"),tbl)

class GraphDlg(gui.Dialog):
    def __init__(self,experimentDone):
        if experimentDone:
            msg = gui.Image(pygame.image.load("graphImg.png"))
        else:
            msg = gui.Label("Complete the experiment first")
        gui.Dialog.__init__(self,gui.Label("Graph"),msg)

##Create a container class with a table attribute
    
class MainGui(gui.Desktop):
    gameAreaWidth = 600
    gameAreaHeight = 400
    gameArea = None
    menuArea = None
    tableArea = None
    # The game engine
    engine = None

    def __init__(self, disp):
        gui.Desktop.__init__(self)
        self.disp = disp
        self.startAnimation = False
        self.paused = False
        self.minVar,self.maxVar = None,None


        # Setup the 'game' area where the action takes place
        self.gameArea = DrawingArea(self.gameAreaWidth,
                                   self.gameAreaHeight)
        # Setup the gui area
        self.menuArea = gui.Container(
            width=disp.get_width()-self.gameAreaWidth, height = self.gameAreaHeight)

        self.tableArea = gui.Table(width = disp.get_width(), height = 200)

        tbl = gui.Table(width=disp.get_width())
        tbl2 = gui.Table(width = self.gameAreaWidth)
        tbl2.tr()
        tbl2.td(self.gameArea)
        tbl2.td(self.menuArea)

        tbl.tr()
        tbl.td(tbl2)
        tbl.tr()
        tbl.td(self.tableArea)

        self.setupMenu()
        self.init(tbl, disp)


    def setupMenu(self):
        buttonWidth = self.menuArea.get_abs_rect().width - 20
        buttonHeight = 30
        tbl = gui.Table()
        
        inputDlg = InputDlg()

        def dialog_cb():
            inputDlg.open()
            
        varBtn = gui.Button("Variables", height = buttonHeight, width = buttonWidth)
        varBtn.connect(gui.CLICK, dialog_cb)
        
        # Add a button for pausing / resuming the game clock
        def startBtn_cb():
            if inputDlg.varsInputted and not(self.startAnimation):
                self.minVar,self.maxVar,self.interval = inputDlg.minVar,inputDlg.maxVar,inputDlg.interval
                self.setupTable()
                self.startAnimation = True
            elif inputDlg.varsInputted and self.startAnimation:
                errorDlg = ErrorDlg("You have already started the experiment")
                errorDlg.open()
            else:
                errorDlg = ErrorDlg("Input variables first")
                errorDlg.open()
                
        startBtn = gui.Button("Start Experiment", height= buttonHeight, width = buttonWidth)
        startBtn.connect(gui.CLICK, startBtn_cb)

        def pauseBtn_cb():
            self.paused = not(self.paused)
            if self.paused:
                pauseBtn.value = "Play Experiment"
            elif not self.paused:
                pauseBtn.value = "Pause Experiment"
            

        pauseBtn = gui.Button("Pause Experiment", height = buttonHeight, width = buttonWidth)
        pauseBtn.connect(gui.CLICK, pauseBtn_cb)

        def restartBtn_cb():
            self.__init__(self.disp)
            self.engine.__init__(self.disp)

        restartBtn = gui.Button("Restart Experiment",height = buttonHeight,width = buttonWidth)
        restartBtn.connect(gui.CLICK, restartBtn_cb)

        def constantsBtn_cb():
            constantsDlg = ConstantsDlg()
            constantsDlg.open()

        constantsBtn = gui.Button("Constants",height = buttonHeight, width = buttonWidth)
        constantsBtn.connect(gui.CLICK, constantsBtn_cb)

            
        graphBtn = gui.Button("Show Graph", height = buttonHeight, width = buttonWidth)
        def graphBtn_cb():
            dlg = GraphDlg(self.engine.experimentDone)
            dlg.open()


            #Run a function which shows the graph and hides the diagram

        graphBtn.connect(gui.CLICK, graphBtn_cb)

        def menuBtn_cb():
            print("MAIN MENU")
##            if self.engine.experimentDone:
##                os.remove("graph.png")
            import MainMenu.MainMenuPGU as m
            m.main()

        menuBtn = gui.Button("Back to Menu", height = buttonHeight, width = buttonWidth)
        menuBtn.connect(gui.CLICK,menuBtn_cb)
        
        btnStyle = {'padding_left':5,'padding_right':5,'padding_top':12,'padding_bottom':12}
        

        tbl.tr()
        tbl.td(graphBtn,style = btnStyle)
        tbl.tr()
        tbl.td(varBtn,style=btnStyle)
        tbl.tr()
        tbl.td(startBtn,style=btnStyle)
        tbl.tr()
        tbl.td(pauseBtn,style=btnStyle)
        tbl.tr()
        tbl.td(restartBtn,style=btnStyle)
        tbl.tr()
        tbl.td(constantsBtn,style = btnStyle)
        tbl.tr()
        tbl.td(menuBtn,style = btnStyle)


        self.menuArea.add(tbl, 0, 0)
        

    def setupTable(self):
        tbl = self.tableArea
        currentNum = self.minVar
        tbl.tr()
        tbl.td(gui.Label("Length of wire"),style={'border':1})

        while currentNum != self.maxVar:
            tbl.td(gui.Label(str(currentNum)),style={'border':1})
            currentNum += self.interval

        tbl.td(gui.Label(str(self.maxVar)),style={'border':1})
        tbl.tr()
        tbl.td(gui.Label("Current(A)"),style={'border':1})
        tbl.tr()
        tbl.td(gui.Label("Resistance()"),style={'border':1})


    def open(self, dlg, pos=None):
        # Gray out the game area before showing the popup
##        rect = self.gameArea.get_abs_rect()
##        dark = pygame.Surface(rect.size).convert_alpha()
##        dark.fill((0,0,0,150))
##        pygame.display.get_surface().blit(dark, rect)
        # Save whatever has been rendered to the 'game area' so we can
        # render it as a static image while the dialog is open.
        self.gameArea.save_background(True)
        # Pause the gameplay while the dialog is visible
        running = not(self.engine.clock.paused)
        self.engine.pause()
        gui.Desktop.open(self, dlg, pos)
        while (dlg.is_open()):
            for ev in pygame.event.get():
                self.event(ev)
            rects = self.update()
            if (rects):
                pygame.display.update(rects)

            if (running):
                # Resume gameplay
                self.engine.resume()

    def get_render_area(self):
        return self.gameArea.get_abs_rect()

    def pauseApp(self):
        self.paused = True

class GameEngine(object):
    def __init__(self,disp):
        self.disp = disp
        self.app = MainGui(self.disp)
        self.app.engine = self
        self.colours = [ORANGE,SILVER]
        self.colourCount = 0
        self.stepCount = 0
        self.minVar = None
        self.maxVar = None
        self.isSetup = False
        self.experimentDone = False
        self.colCount = 1
        self.graphx = []
        self.graphy = []

    # Pause the game clock
    def pause(self):
        self.clock.pause()

    # Resume the game clock
    def resume(self):
        self.clock.resume()

    def render(self, dest, rect):

        self.switchColours()
        wiresColour = self.colours[0]
        IVcolour = self.colours[1]
        
        dest.fill(BLUE,rect)
        battery,batteryRect = setupBattery(rect)
        ruler,rulerRect = setupRuler(batteryRect)
        ammeter,ammeterRect = setupAmmeter(batteryRect)
        voltmeter,voltmeterRect = setupVoltmeter(batteryRect)

        if not(self.app.startAnimation):
            self.crocPoint = [rulerRect.left,batteryRect.center[1] + 300]

        if not(self.isSetup) and self.app.startAnimation:
            self.setupAnimation(self.app.minVar,self.app.maxVar,rulerRect)
            self.calcPoint(rulerRect)
            self.stepCount = 0
            self.colCount += 1


        if self.stepCount == 20 and self.app.startAnimation and not(self.experimentDone):
            self.calcPoint(rulerRect)
            self.stepCount = 0
            self.colCount += 1

        

        #components
        dest.blit(battery, batteryRect.topleft)
        dest.blit(ruler, rulerRect)
        dest.blit(ammeter,ammeterRect)
        dest.blit(voltmeter,voltmeterRect)

        #battery and ammeter wires
        points = []
        points.append((batteryRect.left,batteryRect.center[1]))#left battery
        points.append((batteryRect.left - 200, batteryRect.center[1]))#topleft corner
        points.append((ammeterRect.center[0],ammeterRect.top))#top Ammeter
        pygame.draw.lines(dest,wiresColour,False,points, 3)#draw section
        points = []
        points.append((ammeterRect.center[0],ammeterRect.bottom))#bottom Ammeter

        points.append((batteryRect.left - 200, batteryRect.center[1] + 300))#bottom left corner
        points.append([rulerRect.left - 30,batteryRect.center[1] + 300])#crocLeft.leftside
        pygame.draw.lines(dest,wiresColour,False,points, 3)
        
        points = []
        points.append((self.crocPoint[0],batteryRect.center[1] + 300))
        points.append((self.crocPoint[0],batteryRect.center[1] + 200))#Will need to slide this
        points.append((batteryRect.right + 200, batteryRect.center[1]+ 200))
        points.append((batteryRect.right + 200,batteryRect.center[1]))# top right corner
        points.append((batteryRect.right,batteryRect.center[1]))# right battery
        pygame.draw.lines(dest,wiresColour,False,points, 3)

        #Croc1
        stillCrocPoints = []
        basePoint = [rulerRect.left,batteryRect.center[1] + 300]
        stillCrocPoints.append(basePoint)
        stillCrocPoints.append([basePoint[0] - 30,basePoint[1] - 10])
        stillCrocPoints.append([basePoint[0] - 30,basePoint[1] + 10])
        pygame.draw.polygon(dest, wiresColour, stillCrocPoints, 0)       

        #Wire to be tested
        pygame.draw.line(dest,IVcolour,(rulerRect.left,batteryRect.center[1] + 300),(rulerRect.right,batteryRect.center[1] + 300),3)

        #voltmeter wires
        points = []
        points.append((batteryRect.left - 200, batteryRect.center[1] + 150))
        points.append((voltmeterRect.left,voltmeterRect.center[1]))
        pygame.draw.lines(dest,wiresColour,False,points, 3)
        points = []
        points.append((voltmeterRect.right,voltmeterRect.center[1]))
        points.append((batteryRect.right + 200, voltmeterRect.center[1]))
        pygame.draw.lines(dest,wiresColour,False,points, 3)

        

        #Croc2
        movingCrocPoints = []
        basePoint = self.crocPoint#Will need to slide this point
        movingCrocPoints.append(basePoint)
        movingCrocPoints.append([basePoint[0] + 10,basePoint[1] - 30])
        movingCrocPoints.append([basePoint[0] - 10,basePoint[1] - 30])
        pygame.draw.polygon(dest, wiresColour, movingCrocPoints, 0)     

        return (rect,)

    def setupAnimation(self,minVar,maxVar, rulerRect):
        self.minVar,self.maxVar = minVar,maxVar
        self.currentLength = self.minVar
        self.crocPoint = rulerRect.left + (rulerRect.width * self.minVar/100),rulerRect.center[1] - 20
        self.isSetup = True

    def calcPoint(self,rulerRect):
        self.app.gameArea.save_background(False)
        if self.currentLength == 0:
            self.crocPoint = rulerRect.left,rulerRect.center[1]-20
            current = 0
            resistance = 0
            self.currentLength += self.app.interval
        
        elif self.currentLength >= self.maxVar:
            self.crocPoint = rulerRect.left + (rulerRect.width * self.currentLength/100), rulerRect.center[1] - 20
            current,resistance = genValues(self.currentLength)
            createGraph(self.graphx,self.graphy)
            self.experimentDone = True
        else:
            self.crocPoint = rulerRect.left + (rulerRect.width * self.currentLength/100), rulerRect.center[1] - 20
            current,resistance = genValues(self.currentLength)
            self.currentLength += self.app.interval

        self.graphx.append(self.currentLength)
        self.graphy.append(resistance)
        self.app.tableArea.td(gui.Label(str(current)), col=self.colCount, row=1, style={'border': 1})
        self.app.tableArea.td(gui.Label(str(resistance)), col=self.colCount, row=2, style={'border': 1})



            
    def switchColours(self):
        wiresColour = self.colours[0]
        IVcolour = self.colours[1]
        if self.app.startAnimation and not(self.app.paused):
            self.colourCount += 1
            self.stepCount += 1
            if wiresColour == ORANGE and self.colourCount == 5:
                wiresColour = RED
                IVcolour = ORANGE
                self.colourCount = 0
            elif wiresColour == RED and self.colourCount == 5:
                wiresColour = ORANGE
                IVcolour = SILVER
                self.colourCount = 0

            self.colours = [wiresColour,IVcolour]
    

    def run(self):
        self.app.update(self.disp)
        pygame.display.flip()
        self.font = pygame.font.SysFont("", 16)

        self.clock = timer.Clock()
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
            lst= self.render(self.disp, rect)
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

def setupBattery(rect):
    battery = pygame.image.load(resM.batteryImg)
    battery = pygame.transform.rotate(battery, 90)
    battery = pygame.transform.scale(battery,(60,50))
    batteryRect = battery.get_rect()
    batteryRect.center = rect.center
    batteryRect.center = (batteryRect.center[0],batteryRect.center[1] - rect.height/2 + 50)
    return battery,batteryRect

def setupRuler(batteryRect):    
    ruler = pygame.image.load(resM.rulerImg)
    ruler = pygame.transform.scale(ruler,(300,28))
    rulerRect = ruler.get_rect()
    rulerRect.center = batteryRect.center[0],batteryRect.center[1] + 320
    return ruler,rulerRect

def setupAmmeter(batteryRect):
    ammeter = pygame.image.load(resM.ammeterImg)
    ammeter = pygame.transform.scale(ammeter,(50,50))
    ammeterRect = ammeter.get_rect()
    ammeterRect.center = batteryRect.left - 200, batteryRect.center[1] + 80
    return ammeter,ammeterRect


def setupVoltmeter(batteryRect):
    voltmeter = pygame.image.load(resM.voltmeterImg)
    voltmeter = pygame.transform.scale(voltmeter,(50,50))
    voltmeterRect = voltmeter.get_rect()
    voltmeterRect.center = batteryRect.center[0], batteryRect.center[1] + 150
    return voltmeter,voltmeterRect

def roundUp(num):
    return int(math.ceil(num / 10.0)) * 10

def genValues(currentLength):
    voltage = 1.5
    current = "{0:.3g}".format((voltage * 7.85* 10**-7)/ (1.3 * 10**-6 * currentLength/100))
    resistance = "{0:.3g}".format((voltage/float(current)))
    current = float(current) 
    resistance = float(resistance) 
    current = round(current,3)
    resistance = round(resistance,3)
    return current, resistance


def validateRange(minVar,maxVar,interval):
    resultsValid = True
    print(minVar.isdigit())
    minVar = minVar.replace(" ","")
    maxVar = maxVar.replace(" ","")
    interval = interval.replace(" ","")
    minVarEmpty = minVar == '' 
    maxVarEmpty = maxVar == ''
    intervalEmpty = interval == '' 
    errorMsg = None
    if any([minVarEmpty,maxVarEmpty,intervalEmpty]):
        errorMsg = "Type something in all the boxes"
        return False,minVar,maxVar,interval,errorMsg

    minVarIntCheck = minVar.isdigit()
    maxVarIntCheck = maxVar.isdigit()
    intervalIntCheck = interval.isdigit()
    if all([minVarIntCheck,maxVarIntCheck,intervalIntCheck]) and resultsValid:
        minVar = int(minVar)
        maxVar = int(maxVar)
        interval = int(interval)
    else:
        errorMsg = "You haven't typed only integers"
        return False,minVar,maxVar,interval,errorMsg


    if int(minVar) < 0 and int(maxVar) > 100 and resultsValid:
        errorMsg = "Enter a number between 0 - 100"
        return False,minVar,maxVar,interval,errorMsg
   
    orderCheck = int(maxVar) > int(minVar)
    if not(orderCheck) and resultsValid:        
        errorMsg = "The minimum value should be lower than the maximum"
        return False,minVar,maxVar,interval,errorMsg

    
    if minVar == maxVar and resultsValid:
        errorMsg = "The numbers you have picked are the same"
        return False,minVar,maxVar,interval,errorMsg

    nOfIntervals = (maxVar - minVar)//interval + 1
    if nOfIntervals < 5 and resultsValid:
        errorMsg = "Pick a larger range or smaller intervals to have more than 5 results"
        return False,minVar,maxVar,interval,errorMsg

    if nOfIntervals > 10 and resultsValid:
        errorMsg = "Pick a smaller range or larger intervals to have less than 10 results"
        return False,minVar,maxVar,interval,errorMsg

    intervalMatch = (maxVar - minVar) % interval == 0
    
    if not(intervalMatch):
        errorMsg = "Change the interval or maximum value as the values don't line up"
        return False,minVar,maxVar,interval,errorMsg
        
    
    return True,minVar,maxVar,interval,errorMsg

def createGraph(xVals,yVals):
    plt.scatter(xVals,yVals)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.savefig("graph.png",bbox_inches = 'tight')

 

###
def main():
    disp = pygame.display.set_mode((800, 600))
    eng = GameEngine(disp)
    eng.run()

main()



