import pygame

import Experiments.ExperimentObjects as template
from Experiments.ResistivityOfAMetal import areaObjects
from externalModules.pgu.pgu import gui

# sys.path.append(os.path.abspath('..'))


csa = round(2.01 * 10 ** -8,10)
voltage = 1.5


class Experiment(template.ExperimentTemplate):
    def __init__(self,screen):
        super(Experiment, self).__init__(screen)
        gui.Desktop.__init__(self)
        self.connect(gui.QUIT,self.quit)

        self.engine = None
        self.animationAreaWidth = 650
        self.animationAreaHeight = 400
        self.animationArea = template.DrawingArea(self.animationAreaWidth, self.animationAreaHeight)

        self.menuArea = areaObjects.MenuArea(screen.get_width() - self.animationAreaWidth, self.animationAreaHeight, self)

        self.tableArea = areaObjects.TableArea(screen.get_width(), 200, self)

        self.variablesInputted = False
        self.animationRunning = False
        self.experimentFinished = False

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

    def restart(self):
        run()




def run():
    disp = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("Determination of the Resistivity of a Metal")
    eng = areaObjects.AnimationEngine(disp)
    eng.run()



if __name__ == '__main__':
    run()
