import pygame
import os,sys
sys.path.append(os.path.abspath('../../'))


import Experiments.ExperimentObjects as template
from Experiments.EstimateAbsoluteZero import areaObjects
from externalModules.pgu.pgu import gui


EMF = 4.5
internalResistance = 20


minRange = 10
maxRange = 95

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
    pygame.display.set_caption("Estimating Absolute Zero Using Gas Laws")
    eng = areaObjects.AnimationEngine(disp)
    eng.run()



if __name__ == '__main__':
    run()

