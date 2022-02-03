import pygame

class chatscreen:
    def __init__(self,window,pixelratio):
        self.window = window
        self.pixelratio = pixelratio

        self.validChars = "`123f4567890-=~!@#$% ^&*v()_+qwertyuiop[]\\asdghjxkl'zcbn,./ZXCVBNM<>?ASDFGHJKL:;\"QWERTYUIOP{}|m"

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
