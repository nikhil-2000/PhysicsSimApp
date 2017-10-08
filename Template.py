class DrawingArea(gui.Widget):#Same object as found in gui18.py in the pgu examples
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
    def __init__(self,width,height):
        gui.Table.__init__(self,width= width, height= height)

    def setup(self):
        #This will be run once the user has entered a valid set of variables
        pass

class MenuArea(gui.Container):
    def __init__(self,width,height):
        gui.Container.__init__(self,width=width,height = height)

    def setup(self):
        #All the buttons are created and organised here
        #The function for each will be defined in this method as well
        pass

class Experiment(gui.Desktop):
    def __init__(self,screen):
        self.engine = None
        self.animationAreaWidth = 600
        self.animationAreaHeight = 400
        self.animationArea = DrawingArea(self.animationAreaWidth,self.animationAreaHeight)

        self.menuArea = MenuArea(screen.get_width() - self.animationAreaWidth, self.animationAreaHeight)

        self.tableArea = TableArea(screen.get_width(), screen.get_height() - self.animationAreaHeight)

        screentbl = gui.Table()
        screentbl.tr()
        screentbl.td(self.animationArea)
        screentbl.td(self.menuArea)
        screentbl.tr()
        screentbl.td(self.tableArea)

        self.menuArea.setup()

        self.init(screentbl,screen)

        def open(self, dlg, pos=None):#Same method as found in gui18.py in the pgu examples
            self.gameArea.save_background()
            # Pause the gameplay while the dialog is visible
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
                    # Resume gameplay
                    self.engine.resume()

        def get_render_area(self):
            return self.gameArea.get_abs_rect()


class Animation(object):
    def __init__(self, disp):
        self.disp = disp
        self.app = Experiment(self.disp)
        self.app.engine = self



    def render(self, dest, rect):

        #Drawing logic should go here

        return (rect,)

    def setupAnimation(self, minVar, maxVar, rulerRect):
        #Called once the user has entered correct variables
        pass

    def run(self):#This function is taken from the gui18.py which is in the pgu module under examples
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
            self.disp.set_clip(rect)

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
    eng = GameEngine(disp)
    eng.run()
