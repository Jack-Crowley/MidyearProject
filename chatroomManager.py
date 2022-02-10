import pygame
from shapes import *
class Chatroom:
    def __init__(self, window, clock, pixelratio,validChars, client):
        self.window = window

        self.clock = clock
        self.pixelratio = pixelratio

        print(self.pixelratio)

        self.client = client

        self.messageQueue = []

        self.validChars = validChars

        self.chatroomclickables = []
        self.chatroomdrawables = []
        self.chatroommessages = []

        self.loadDrawables()

        self.run = True
        
        self.exitButtons = [pygame.transform.scale(pygame.image.load("Images\\x_black.png"), (20/self.pixelratio, 20/self.pixelratio)), pygame.transform.scale(pygame.image.load("Images\\x.png"), (20/self.pixelratio, 20/self.pixelratio))]

        self.active = None

        self.textboxy = 1000
        self.textboxlinecount = 0

        while self.run:
            if self.messageQueue != []:
                msg = client.send_message(self.messageQueue[0])
                del(self.messageQueue[0])
            else:
                msg = client.send_message("")
            if msg != 0:
                msg = msg.split(":")
                self.createNewMessage(msg[0],''.join(msg[1:]))
            self.clock.tick(60)
            mousex,mousey = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
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
                            elif button.command == "exit":
                                if button.click(mousex,mousey):
                                    print('exited')
                                    self.run = False
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
            pygame.display.update()
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
        mousex,mousey = pygame.mouse.get_pos()
        self.window.fill((27,27,27))
        for i in self.chatroomdrawables: i.draw()
        for i in self.chatroommessages: i.draw()
        if 1900/self.pixelratio <= mousex and 0 <= mousey <= 20/self.pixelratio:
            self.window.blit(self.exitButtons[1], (1900/self.pixelratio,0))
        else:
            self.window.blit(self.exitButtons[0], (1900/self.pixelratio,0))
        pygame.display.update()
    
    def loadDrawables(self):
        self.chatroomdrawables.append(Rectangle(0,100,1920,5,(2,217,198),self.window,self.pixelratio))
        self.chatroomdrawables.append(Rectangle(400,100,5,980,(2,217,198),self.window,self.pixelratio))
        self.chatroomdrawables.append(Text("Orbitron",(193,146,252),"USERS",self.window,200,175,self.pixelratio,75))
        self.chatroomdrawables.append(Rectangle(75,200,250,10,(193,146,252),self.window,self.pixelratio))
        self.createInputField(450,1000,1000,30,(17,17,17),self.window,self.pixelratio,"input_field",(2,217,198),"wrap","Enter Text Here...",(193,146,252),self.validChars,30)
        self.createButton(1900,0,20,20,(0,0,0),self.window,self.pixelratio,"exit")

    def createInputField(self,x,y,width,height,color,window,pixelratio,command,textcolor,mode,emptyMessage,cursorColor,validChars,size):
        tempInputField = InputField(x,y,width,height,color,window,pixelratio,command,textcolor,mode,emptyMessage,cursorColor,validChars,size)
        self.chatroomdrawables.append(tempInputField)
        self.chatroomclickables.append(tempInputField)

    def createButton(self,x,y,width,height,color,window,pixelratio,command):
        tempButton = Button(x,y,width,height,color,window,pixelratio,command)
        self.chatroomdrawables.append(tempButton)
        self.chatroomclickables.append(tempButton)

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

    def createNewMessage(self,username,msg):
        a = messageObject(450,self.textboxy,1000,(255,255,255),self.window,self.pixelratio,username,msg,30)
        for i in self.chatroommessages:
            i.indepenty += a.height/self.pixelratio
        self.chatroommessages.append(a)
        if self.active != None:
            self.active.y = 1000/self.pixelratio

    def send(self):
        newtext = self.active.getStr()
        self.messageQueue.append(newtext)