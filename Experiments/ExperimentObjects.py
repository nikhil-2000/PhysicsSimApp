import os
import sys
sys.path.append(os.path.abspath('..'))

#The previous lines were taken from https://stackoverflow.com/questions/10272879/how-do-i-import-a-python-script-from-a-sibling-directory
#It explained how to access modules in sibling directories

import pygame
from externalModules.pgu.pgu import gui, timer



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


class TableArea(gui.Table):
    def __init__(self, width, height, app):
        gui.Table.__init__(self, width=width, height=height)
        self.app = app

    def setup(self):
        pass


# This will be run once the user has entered a valid set of variables

class MenuArea(gui.Table):
    def __init__(self, width, height, app):
        gui.Table.__init__(self, width=width, height=height)
        self.app = app

    def setup(self):
        # All the buttons are created and organised here
        # The function for each will be defined in this method as well
        def menuBtn_cb():
            pygame.quit()
            import MainMenu as m
            m.run()

        menuBtn = gui.Button("Back to Menu",width= 150, height = 50)
        menuBtn.connect(gui.CLICK,menuBtn_cb)
        self.tr()
        self.td(menuBtn)




class Experiment(gui.Desktop):
    def __init__(self, screen):
        gui.Desktop.__init__(self)
        self.connect(gui.QUIT,self.quit)

        self.engine = None
        self.animationAreaWidth = 600
        self.animationAreaHeight = 400
        self.animationArea = DrawingArea(self.animationAreaWidth, self.animationAreaHeight)

        self.menuArea = MenuArea(screen.get_width() - self.animationAreaWidth, self.animationAreaHeight, self)

        self.tableArea = TableArea(screen.get_width(), 200, self)

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

        self.menuArea.setup()

        self.init(screenTbl, screen)

    def open(self, dlg, pos=None):  # Same method as found in gui18.py in the pgu examples
        self.gameArea.save_background()  # Pause the gameplay while the dialog is visible
        running = not (self.engine.clock.paused)
        self.engine.pause()
        gui.Desktop.open(self, dlg, pos)
        while (dlg.is_open()):
            for ev in pygame.event.get():
                self.event(ev)
            rects = self.update()
            if (rects):
                pygame.display.update(rects)
            if (running):
                self.engine.resume()  # Resume gameplay


    def get_render_area(self):
        return self.animationArea.get_abs_rect()


class AnimationEngine(object):
    def __init__(self, disp):
        self.disp = disp
        self.app = Experiment(self.disp)
        self.app.engine = self

    def render(self, dest, rect):

        # Drawing code should go here

        return (rect,)

    def setupAnimation(self):
        # Called once the user has entered correct variables
        pass

    def run(self):  # This function is taken from the gui18.py which is in the pgu module under examples
        self.app.update(self.disp)
        pygame.display.flip()

        self.clock = timer.Clock()
        done = False

        while not done:
            for event in pygame.event.get():
                quitBool = (event.type == pygame.QUIT) or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
                if quitBool:
                    done = True
                else:
                    self.app.event(event)

            rect = self.app.get_render_area()
            updates = []
            self.disp.set_clip(rect)
            lst = self.render(self.disp, rect)
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




def main():
    disp = pygame.display.set_mode((800, 600))
    eng = AnimationEngine(disp)
    eng.run()
