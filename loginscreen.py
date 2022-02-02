import pygame
from shapes import *

class Login:
    def __init__(self,window):
        

        self.window = window

        self.MWIDTH, self.MHEIGHT = self.window.get_size()
        self.pixelratio = 1920/self.MWIDTH

        self.drawables=[]
        self.clickables = []
        self.loadDrawables()
        self.active = None
        self.run = True
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousex,mousey = pygame.mouse.get_pos()
                    for button in self.clickables:
                        button.deactivate()
                        button.color = (17,17,17)
                        if button.click(mousex,mousey):
                            if button.command == "input_field":
                                button.activate()
                                self.active = button
                                button.color = (35,35,35)
                if event.type == pygame.KEYDOWN:
                    if self.active != None:
                        if event.key == pygame.K_BACKSPACE:
                            self.active.delChar()
                        elif event.unicode in "`123f4567890-=~!@#$% ^&*()_+qwertyuiop[]\\asdghjkl'zcbn,./ZXCVBNM<>?ASDFGHJKL:\"QWERTYUIOP{}|m":
                            self.active.addChar(event.unicode)
                            
            
            self.draw()
        
    def loadDrawables(self):
        self.drawables.append(Rectangle(0,0,1920,192,(17,17,17),self.window,self.pixelratio))
        self.drawables.append(Rectangle(576,300,768,700,(17,17,17),self.window,self.pixelratio))
        self.drawables.append(Text("Orbitron",(193,146,252),"PERMEABILITY",self.window,1067,96,self.pixelratio,192))
        self.drawables.append(Text("Orbitron",(2,217,198),"LOG IN TO CONTINUE",self.window,960,350,self.pixelratio,75))
        self.drawables.append(Rectangle(726,550,468,15,(2,217,198),self.window,self.pixelratio))
        self.drawables.append(Image("Images\purple_log_header.png",390,10,150,150,self.window,self.pixelratio))
        self.createInputField(726,475,468,75,(17,17,17),self.window,self.pixelratio,"input_field",(2,217,198),"scroll","Enter Username...")

        self.createInputField(726,600,468,75,(17,17,17),self.window,self.pixelratio,"input_field",(2,217,198),"scroll","Enter Password...")
        self.drawables.append(Rectangle(726,675,468,15,(2,217,198),self.window,self.pixelratio))

    def createButton(self,x,y,width,height,color,window,pixelratio,command):
        tempButton = Button(x,y,width,height,color,window,pixelratio,command)
        self.drawables.append(tempButton)
        self.clickables.append(tempButton)

    def createInputField(self,x,y,width,height,color,window,pixelratio,command,textcolor,mode,emptyMessage):
        tempInputField = InputField(x,y,width,height,color,window,pixelratio,command,textcolor,mode,emptyMessage,)
        self.drawables.append(tempInputField)
        self.clickables.append(tempInputField)


    def draw(self):
        self.window.fill((27,27,27))
        for i in self.drawables:
            i.draw()
        pygame.display.update()