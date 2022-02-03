import pygame
from shapes import *
class Chatroom:
    def __init__(self, window, clock, pixelratio,validChars):
        self.window = window

        self.clock = clock
        self.pixelratio = pixelratio

        self.validChars = validChars

        self.chatroomclickables = []
        self.chatroomdrawables = []

        self.loadDrawables()

        self.run = True
        


        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            self.draw()
    
    def draw(self):
        self.window.fill((27,27,27))
        for i in self.chatroomdrawables:
            i.draw()
        pygame.display.update()
    
    def loadDrawables(self):
        self.chatroomdrawables.append(Rectangle(0,100,1920,5,(2,217,198),self.window,self.pixelratio))
        self.chatroomdrawables.append(Rectangle(400,100,5,980,(2,217,198),self.window,self.pixelratio))
        self.chatroomdrawables.append(Text("Orbitron",(193,146,252),"USERS",self.window,200,175,self.pixelratio,75))
        self.chatroomdrawables.append(Rectangle(75,200,250,10,(193,146,252),self.window,self.pixelratio))
        self.createInputField(450,800,1000,200,(17,17,17),self.window,self.pixelratio,"input_field",(2,217,198),"scroll","Enter Text Here...",(193,146,252),self.validChars)

    def createInputField(self,x,y,width,height,color,window,pixelratio,command,textcolor,mode,emptyMessage,cursorColor,validChars):
        tempInputField = InputField(x,y,width,height,color,window,pixelratio,command,textcolor,mode,emptyMessage,cursorColor,validChars)
        self.chatroomdrawables.append(tempInputField)
        self.chatroomclickables.append(tempInputField)