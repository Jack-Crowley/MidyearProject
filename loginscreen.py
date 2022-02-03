import pygame
from shapes import *

class Login:
    def __init__(self,window,clock):
        

        self.window = window
        self.clock = clock

        self.MWIDTH, self.MHEIGHT = self.window.get_size()
        self.pixelratio = 1920/self.MWIDTH

        self.validChars = "`123f4567890-=~!@#$% ^&*v()_+qwertyuiop[]\\asdghjxkl'zcbn,./ZXCVBNM<>?ASDFGHJKL:;\"QWERTYUIOP{}|m"

        self.drawables=[]
        self.clickables = []
        self.loadDrawables()
        self.active = None
        self.run = True
        while self.run:
            self.clock.tick(60)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousex,mousey = pygame.mouse.get_pos()
                    for button in self.clickables:
                        if button.command == "input_field":
                                button.deactivate()
                                button.active = False
                                button.color = (17,17,17)
                                if button.click(mousex,mousey):
                                    button.activate()
                                    self.active = button
                                    button.active = True
                                    button.color = (35,35,35)
                        elif button.command == "new_screen":
                            if button.click(mousex,mousey):
                                    self.run = False
                if self.active != None:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.active.delChar()
                        elif event.key == pygame.K_LEFT:
                            self.active.moveCursorLeft()
                        elif event.unicode in self.validChars:
                            self.active.addChar(event.unicode)
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_BACKSPACE:
                            self.active.backspacevelocity = 1
                            self.active.backspacecounter = 0
                        elif event.unicode in self.validChars:
                            self.active.lettercounter[event.unicode] = 0
                            self.active.lettervelocity[event.unicode] = 1
            if self.active != None:
                if keys[pygame.K_BACKSPACE]:
                    self.active.backspace()
                for i in self.validChars:
                    if keys[ord(i)]:
                        self.active.letter(i)
                    
            
            self.draw()
        
    def loadDrawables(self):
        self.drawables.append(Rectangle(0,0,1920,192,(17,17,17),self.window,self.pixelratio))
        self.drawables.append(Rectangle(576,300,768,700,(17,17,17),self.window,self.pixelratio))
        self.drawables.append(Text("Orbitron",(193,146,252),"PERMEABILITY",self.window,1067,96,self.pixelratio,192))
        self.drawables.append(Text("Orbitron",(2,217,198),"LOG IN TO CONTINUE",self.window,960,350,self.pixelratio,75))
        self.drawables.append(Rectangle(726,550,468,15,(2,217,198),self.window,self.pixelratio))
        self.drawables.append(Image("Images\purple_log_header.png",390,10,150,150,self.window,self.pixelratio))
        self.createInputField(726,475,468,75,(17,17,17),self.window,self.pixelratio,"input_field",(2,217,198),"scroll","Enter Username...",(193,146,252),self.validChars)

        self.createInputField(726,600,468,75,(17,17,17),self.window,self.pixelratio,"input_field",(2,217,198),"password","Enter Password...",(193,146,252),self.validChars)
        self.drawables.append(Rectangle(726,675,468,15,(2,217,198),self.window,self.pixelratio))

        self.createButton(726,825,468,75,(193,146,252),self.window,self.pixelratio,command="new_screen")
        self.drawables.append(Text("Orbitron",(255,255,255), "LOGIN",self.window,960,862,self.pixelratio,75))

    def createButton(self,x,y,width,height,color,window,pixelratio,command):
        tempButton = Button(x,y,width,height,color,window,pixelratio,command)
        self.drawables.append(tempButton)
        self.clickables.append(tempButton)

    def createInputField(self,x,y,width,height,color,window,pixelratio,command,textcolor,mode,emptyMessage,cursorColor,validChars):
        tempInputField = InputField(x,y,width,height,color,window,pixelratio,command,textcolor,mode,emptyMessage,cursorColor,validChars)
        self.drawables.append(tempInputField)
        self.clickables.append(tempInputField)


    def draw(self):
        self.window.fill((27,27,27))
        for i in self.drawables:
            i.draw()
        pygame.display.update()