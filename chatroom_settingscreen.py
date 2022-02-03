import pygame

class settingscreen:
    def __init__(self,window,pixelRatio):
        self.window = window
        self.pixelratio = pixelRatio
        self.drawables=[]
        self.clickables = []
        self.loadDrawables()
        self.active = None
        
    def draw(self):
        self.window.fill((27,27,27))
        for i in self.drawables:
            i.draw()
        pygame.display.update()
        
    def loadDrawables(self):
        pass
