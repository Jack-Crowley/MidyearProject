import pygame
from shapes import *
class Chatroom:
    def __init__(self, window, clock, pixelratio,validChars, client):
        self.window = window

        self.clock = clock
        self.pixelratio = pixelratio

        self.client = client

        self.validChars = validChars

        self.chatroomclickables = []
        self.chatroomdrawables = []
        self.chatroommessages = []

        self.loadDrawables()

        self.run = True
        
        self.active = None

        self.textboxy = 1000
        self.textboxlinecount = 0

        while self.run:
            self.clock.tick(60)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousex,mousey = pygame.mouse.get_pos()
                    for button in self.chatroomclickables:
                        if button.command == "input_field":
                                button.deactivate()
                                button.active = False
                                button.color = (17,17,17)
                                if button.click(mousex,mousey):
                                    button.activate()
                                    self.active = button
                                    button.active = True
                                    button.color = (35,35,35)
                if self.active != None:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.active.delChar()
                        elif event.key == pygame.K_LEFT:
                            self.active.moveCursorLeft()
                        elif event.key == pygame.K_RETURN:
                            self.send()
                            self.newMessage()
                        elif event.unicode in self.validChars:
                            self.active.addChar(event.unicode)
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_BACKSPACE:
                            self.active.backspacevelocity = 1
                            self.active.backspacecounter = 0
                        elif event.key == pygame.K_RIGHT:
                            self.active.rightarrowcount = 0
                            self.active.rightarrowvecolicty = 1
                        elif event.key == pygame.K_LEFT:
                            self.active.leftarrowcount = 0
                            self.active.leftarrowvelocity = 1
                        elif event.unicode in self.validChars:
                            self.active.lettercounter[event.unicode] = 0
                            self.active.lettervelocity[event.unicode] = 1
            if self.active != None:
                self.textboxy = self.active.y
                for i in self.chatroommessages:
                    i.y = self.textboxy-(35/pixelratio*(len(i.messages)-2))
                if keys[pygame.K_BACKSPACE]:
                    self.active.backspace()
                if keys[pygame.K_LEFT]:
                    self.active.left()
                if keys[pygame.K_RIGHT]:
                    self.active.right()
                for i in self.validChars:
                    if keys[ord(i)]:
                        self.active.letter(i)
            self.draw()
    
    def draw(self):
        self.window.fill((27,27,27))
        for i in self.chatroomdrawables: i.draw()
        for i in self.chatroommessages: i.draw()
        pygame.display.update()
    
    def loadDrawables(self):
        self.chatroomdrawables.append(Rectangle(0,100,1920,5,(2,217,198),self.window,self.pixelratio))
        self.chatroomdrawables.append(Rectangle(400,100,5,980,(2,217,198),self.window,self.pixelratio))
        self.chatroomdrawables.append(Text("Orbitron",(193,146,252),"USERS",self.window,200,175,self.pixelratio,75))
        self.chatroomdrawables.append(Rectangle(75,200,250,10,(193,146,252),self.window,self.pixelratio))
        self.createInputField(450,1000,1000,30,(17,17,17),self.window,self.pixelratio,"input_field",(2,217,198),"wrap","Enter Text Here...",(193,146,252),self.validChars,30)

    def createInputField(self,x,y,width,height,color,window,pixelratio,command,textcolor,mode,emptyMessage,cursorColor,validChars,size):
        tempInputField = InputField(x,y,width,height,color,window,pixelratio,command,textcolor,mode,emptyMessage,cursorColor,validChars,size)
        self.chatroomdrawables.append(tempInputField)
        self.chatroomclickables.append(tempInputField)

    def newMessage(self):
        newtext = self.active.getStr()
        a = messageObject(450,self.textboxy,1000,(255,255,255),self.window,self.pixelratio,"test",newtext,30)
        for i in self.chatroommessages:
            i.indepenty += a.height/self.pixelratio
        self.active.fullMSG = ""
        self.chatroommessages.append(a)
        self.active.textMessage = ""
        self.active.textList = []
        self.active.linecount=0
        self.active.y = 1000/self.pixelratio

    def send(self):
        newtext = self.active.getStr()
        print(newtext)
        self.client.send(newtext)