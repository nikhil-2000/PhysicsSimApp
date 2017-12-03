import os
import sys
import externalModules.pgu.pgu.gui as gui
sys.path.append(os.path.abspath('..'))

import Experiments.ExperimentObjects as template
import Experiments.creatingGraphs as graph
import pygame

class GraphDialog(gui.Dialog):
    def __init__(self,xPoints,yPoints):
        gradient,yIntercept = graph.createGraph(xPoints,yPoints)
        gradientLbl = gui.Label(str(round(gradient,3)))
        yInterceptLbl = gui.Label(str(round(yIntercept,3)))

        tbl = gui.Table()
        tbl.tr()
        tbl.td(gui.Image("graph.png"))
        tbl.tr()
        tbl.td(gradientLbl)
        tbl.tr()
        tbl.td(yInterceptLbl)

        gui.Dialog.__init__(self,gui.Label("Graph"),tbl)



class TableArea(template.TableAreaTemplate):
    def __init__(self,width,height,app):
        super(TableArea, self).__init__(width,height,app)


class MenuArea(template.MenuAreaTemplate):
    def __init__(self,width,height,app):
        super(MenuArea, self).__init__(width,height,app)
        self.setupButtons()
        print("KJKKJKJK")

    def setupButtons(self):
        self.setup()

        def graph_cb():
            print("JKJ")
            if self.app.experimentFinished:
                graphDlg = GraphDialog(xPoints,yPoints)
                self.open(graphDlg)
            else:
                errorDlg = template.ErrorDlg("Finish the Experiment")
                self.app.open(errorDlg)

        self.graphBtn.connect(gui.CLICK,graph_cb)

        def variables_cb():
            variablesDlg = template.VariablesDialog(["10,100,10"],0,100)
            self.open(variablesDlg)

        self.variablesBtn.connect(gui.CLICK,variables_cb)

class Experiment(template.ExperimentTemplate):
    def __init__(self,screen):
        super(Experiment, self).__init__(screen)
        gui.Desktop.__init__(self)
        self.connect(gui.QUIT,self.quit)

        self.engine = None
        self.animationAreaWidth = 650
        self.animationAreaHeight = 400
        self.animationArea = template.DrawingArea(self.animationAreaWidth, self.animationAreaHeight)

        self.menuArea = MenuArea(screen.get_width() - self.animationAreaWidth, self.animationAreaHeight, self)

        self.tableArea = TableArea(screen.get_width(), 200, self)

        self.variablesInputted = False
        self.animationRunning = False
        self.experimentFinished = False

        screentbl = gui.Table()
        topTbl = gui.Table()
        topTbl.tr()
        topTbl.td(self.animationArea)
        topTbl.td(self.menuArea)
        screenTbl = gui.Table(height= screen.get_height(), width = screen.get_width())

        screenTbl.tr()
        screenTbl.td(topTbl)
        screenTbl.tr()
        screenTbl.td(self.tableArea)

        self.init(screenTbl, screen)

class AnimationEngine(template.AnimationEngineTemplate):
    def __init__(self, disp):
        super(AnimationEngine, self).__init__(disp)
        self.app = Experiment(self.disp)
        self.app.engine = self

    def render(self, dest, rect):

        return (rect,)


def run():
    disp = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("Determination of the Resistivity of a Metal")
    eng = AnimationEngine(disp)
    eng.run()


if __name__ == '__main__':
    run()
