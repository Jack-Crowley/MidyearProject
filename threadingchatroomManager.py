import pygame
import threading
from shapes import *
class Chatroom:
    def __init__(self, window, clock, pixelratio,validChars,client, username):
        self.window = window

        self.clock = clock
        self.pixelratio = pixelratio

        self.validChars = validChars

        self.miny = -200
        self.maxy = 930

        self.downarrowcount, self.downarrowvelocity = 0, 1
        self.uparrowcount, self.uparrowvelocity = 0, 1

        self.username = username

        self.client = client

        self.chatroomclickables = []
        self.chatroomdrawables = []
        self.chatroommessages = []
        self.userslist = []
        self.loadDrawables()

        self.run = True
        
        self.exitButtons = [pygame.transform.scale(pygame.image.load("Images\\x_black.png"), (int(40/self.pixelratio), int(40/self.pixelratio))), pygame.transform.scale(pygame.image.load("Images\\x.png"), (int(40/self.pixelratio), int(40/self.pixelratio)))]

        self.active = None

        self.textboxy = 1000
        self.textboxlinecount = 0
        self.scrolly = 0

        self.buttonsClicked = 0

        msg = ""
        sending = threading.Thread(target = self.client.send_message, args = (msg,), daemon = True)
        sending.start()
        recieving = threading.Thread(target = self.client.recieve_message, args = (), daemon = True)
        recieving.start()

        while self.run:
            self.clock.tick(60)
            if len(self.client.recievingQueue) != 0:
                self.createNewMessage(self.client.recievingQueue[0][0], self.client.recievingQueue[0][1])
                del self.client.recievingQueue[0]
            mousex,mousey = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.chatroomclickables:
                            self.buttonsClicked += 1
                            if button.command == "input_field":
                                    button.deactivate()
                                    button.active = False
                                    button.color = (35,35,35)
                                    if button.click(mousex,mousey):
                                        self.buttonsClicked -= 1
                                        button.activate()
                                        self.active = button
                                        button.active = True
                                        button.color = (50,50,50)                       
                            if button.command == "exit":
                                if button.click(mousex,mousey):
                                    print('exited')
                                    self.run = False
                    if self.buttonsClicked == len(self.chatroomclickables):
                        self.active = None
                    self.buttonsClicked = 0
                    
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
                        elif event.key == pygame.K_DOWN:
                            self.downarrowcount = 0
                            self.downarrowvelocity = 1
                        elif event.key == pygame.K_UP:
                            self.uparrowcount = 0
                            self.uparrowvelocity = 1
                        elif event.unicode in self.validChars:
                            self.active.lettercounter[event.unicode] = 0
                            self.active.lettervelocity[event.unicode] = 1
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                            if len(self.chatroommessages):
                                if self.chatroommessages[0].y < 1000:
                                    print(self.chatroommessages[-1].y)
                                    self.moveBox(-20)
                    elif event.key == pygame.K_DOWN:
                        if self.scrolly > 0:
                            self.moveBox(20)            
            if self.active != None:
                self.textboxy = self.active.y
                for i in self.chatroommessages:
                    i.y = self.textboxy-(35/pixelratio*(len(i.messages)-2))-10
                if keys[pygame.K_BACKSPACE]:
                    self.active.backspace()
                if keys[pygame.K_LEFT]:
                    self.active.left()
                if keys[pygame.K_RIGHT]:
                    self.active.right()
                for i in self.validChars:
                    if keys[ord(i)]:
                        self.active.letter(i)
            if keys[pygame.K_UP]:
                self.up()
            if keys[pygame.K_DOWN]:
                self.down()
            self.draw()
    
    def draw(self):
        self.updateUserList()
        mousex,mousey = pygame.mouse.get_pos()
        self.window.fill((27,27,27))
        for i in self.chatroommessages:  i.draw()
        for i in self.chatroomdrawables: i.draw()
        for i in self.userslist: i.draw()
        if 1880/self.pixelratio <= mousex and 0 <= mousey <= 40/self.pixelratio:
            self.window.blit(self.exitButtons[1], (1880/self.pixelratio,0))
        else:
            self.window.blit(self.exitButtons[0], (1880/self.pixelratio,0))
        pygame.display.update()
    
    def loadDrawables(self):
        self.chatroomdrawables.append(Rectangle(0,0,1920,100,(12,12,12),self.window,self.pixelratio))
        self.chatroomdrawables.append(Rectangle(0,100,1920,5,(2,217,198),self.window,self.pixelratio))
        self.chatroomdrawables.append(Rectangle(400,100,5,980,(2,217,198),self.window,self.pixelratio))
        self.chatroomdrawables.append(Text("Orbitron",(193,146,252),"USERS",self.window,200,175,self.pixelratio,75))
        self.chatroomdrawables.append(Rectangle(75,200,250,10,(193,146,252),self.window,self.pixelratio))
        self.chatroomdrawables.append(Rectangle(450,1000,1000,80,(27,27,27),self.window,self.pixelratio))
        self.createInputField(450,990,1000,40,(35,35,35),self.window,self.pixelratio,"input_field",(2,217,198),"wrap","Enter Text Here...",(193,146,252),self.validChars,40)
        self.createButton(1880,0,40,40,(0,0,0),self.window,self.pixelratio,"exit")
        
    def updateUserList(self):
        print(self.client.userList)
        self.userslist = []
        for i in self.client.userList:
            for x in self.userslist: x.y += 150
            self.userslist.append(User(i, self.window))

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
        a = messageObject(450,self.textboxy,1000,(255,255,255),self.window,self.pixelratio,self.username,newtext,30, (193,146,252))
        if len(self.chatroommessages) != 0:
            print("true")
            a.indepenty = self.chatroommessages[-1].indepenty
        for i in self.chatroommessages:
            i.indepenty += a.height/self.pixelratio
            i.relativey += a.height/self.pixelratio
        self.active.fullMSG = ""
        self.chatroommessages.append(a)
        self.active.textMessage = ""
        self.active.textList = []
        self.active.linecount=0
        self.active.y = 1000/self.pixelratio
        self.active.cursorIndex = 0

    def createNewMessage(self,username,msg):
        a = messageObject(450,self.textboxy,1000,(255,255,255),self.window,self.pixelratio,username,msg,30, (2,217,198))
        if len(self.chatroommessages) != 0:
            print("true")
            a.indepenty = self.chatroommessages[-1].indepenty
        for i in self.chatroommessages:
            i.indepenty += a.height/self.pixelratio
            i.relativey += a.height/self.pixelratio
        self.chatroommessages.append(a)
        if self.active != None:
            self.active.y = 1000/self.pixelratio

    def send(self):
        newtext = self.active.getStr()
        self.client.messageQueue.append(newtext)

    def moveBox(self, num):
        for i in self.chatroommessages:
            i.indepenty += num
        self.scrolly -= num
    
    def down(self):
        if self.scrolly > 0:
            self.downarrowcount += 0.07*self.downarrowvelocity
            if self.downarrowcount > 1:
                self.downarrowcount = 0
                self.downarrowvelocity += 0.5
                self.moveBox(20)
    
    def up(self):
        print(self.uparrowcount)
        self.uparrowcount += 0.07*self.uparrowvelocity
        if self.uparrowcount > 1:
            self.uparrowcount = 0
            self.uparrowvelocity += 0.5
            if len(self.chatroommessages):
                if self.chatroommessages[0].indepenty > 50:
                    print(self.chatroommessages[0].indepenty, "y value")
                    self.moveBox(-20)