from pyexpat.errors import messages
import pygame

class Rectangle:
    def __init__(self,x,y,width,height,color,window,pixelratio):
        self.x=x/pixelratio
        self.y=y/pixelratio
        self.width=width/pixelratio
        self.height=height/pixelratio
        self.color=color
        self.window=window
    
    def draw(self):
        pygame.draw.rect(self.window,self.color,(self.x,self.y,self.width,self.height))

class Button:
    def __init__(self,x,y,width,height,color,window,pixelratio,command):
        self.x=x/pixelratio
        self.y=y/pixelratio
        self.width=width/pixelratio
        self.height=height/pixelratio
        self.color=color
        self.window=window
        self.command = command
    
    def draw(self):
        pygame.draw.rect(self.window,self.color,(self.x,self.y,self.width,self.height))
    
    def click(self,mx,my):
        if self.x <= mx <= self.x+self.width and self.y <= my <= self.y+self.height:
            return True
        return False

class InputField:
    def __init__(self,x,y,width,height,color,window,pixelratio,command,textcolor,mode,emptyMessage,cursorColor,validChars,size):
        self.x=x/pixelratio
        self.y=y/pixelratio
        self.width=width/pixelratio
        self.height=height/pixelratio
        self.size = size/pixelratio
        self.color=color
        self.window=window
        self.active = False
        self.command = command
        self.textcolor = textcolor
        self.emptyMessage=emptyMessage
        self.textMessage = emptyMessage
        self.cursorColor = cursorColor
        self.cursorIndex = 0
        self.mode = mode
        self.currentIndex = 0
        self.maxCurrentIndex = -1
        self.lettercounter = {char:0 for char in validChars}
        self.lettervelocity = {char:1 for char in validChars}
        self.backspacecounter = 0
        self.backspacevelocity = 1
        self.leftarrowvelocity = 1
        self.leftarrowcount = 0
        self.rightarrowcount = 0
        self.rightarrowvecolicty = 1
        self.linecount=0
        self.fullMSG = ""
        self.textList = []
        self.textMessageList = []
        self.text = pygame.font.SysFont("Orbitron", int(self.size))
        self.changeText()
    
    def draw(self):
        if self.mode == "scroll" or self.mode == "password":
            pygame.draw.rect(self.window,self.color,(self.x,self.y,self.width,self.height))
            self.updateCursor()
            self.changeText()
            self.window.blit(self.textObject,(self.x,self.y+(self.textObject.get_height()//2)))
        else:
            pygame.draw.rect(self.window,self.color,(self.x,self.y,self.width,self.height+(self.size*self.linecount)))
            self.updateCursor()
            self.changeText()
            for i in range(self.linecount):
                self.window.blit(self.textList[i],(self.x,self.y+(i*self.size)+(self.textObject.get_height()//2)))
            self.window.blit(self.textObject,(self.x,self.y+(self.size*self.linecount)))
    
    def click(self,mx,my):
        if self.x <= mx <= self.x+self.width and self.y <= my <= self.y+self.height+(self.size*self.linecount):
            return True
        return False
    
    def changeText(self):
        if self.mode == "scroll":
            self.textObject = self.text.render(self.textMessage[self.currentIndex:self.maxCurrentIndex], False, self.textcolor)
            while self.textObject.get_width() > self.width - 5:
                self.currentIndex+=1
                self.textObject = self.text.render(self.textMessage[self.currentIndex:self.maxCurrentIndex], False, self.textcolor)
        elif self.mode == "password":
            if self.textMessage != self.emptyMessage:
                self.textObject = self.text.render(len(self.textMessage[self.currentIndex:self.maxCurrentIndex])*"*", False, self.textcolor)
                while self.textObject.get_width() > self.width - 5:
                    self.currentIndex+=1
                    self.textObject = self.text.render(len(self.textMessage[self.currentIndex:self.maxCurrentIndex])*"*", False, self.textcolor)
            else:
                self.textObject = self.text.render(self.textMessage[self.currentIndex:self.maxCurrentIndex], False, self.textcolor)
        elif self.mode == "wrap":
            self.textObject = self.text.render(self.textMessage, False, self.textcolor)
            if self.textObject.get_width() > self.width - 5:
                self.textList.append(self.textObject)
                self.textMessageList.append(self.textMessage[:-1])
                self.fullMSG += self.textMessage[:-1]
                self.textMessage = self.textMessage[-1]
                self.linecount += 1
                self.cursorIndex = 1
                self.y-=self.height
                self.textObject = self.text.render(self.textMessage, False, self.textcolor)

        

    def activate(self):
        if self.textMessage == self.emptyMessage:
            self.textMessage = ""
            self.maxCurrentIndex = 0
        self.changeText()
    
    def deactivate(self):
        if self.textMessage == "":
            self.textMessage = self.emptyMessage
            self.maxCurrentIndex = -1
        self.changeText()

    def addChar(self,char):
        if self.mode == "wrap":
            if self.linecount <= 12:
                self.textMessage = self.textMessage[:self.cursorIndex] + char + self.textMessage[self.cursorIndex:]
                self.cursorIndex+=1
                self.maxCurrentIndex += 1
                self.changeText()
        else:
            if len(self.textMessage) <= 10:
                self.textMessage = self.textMessage[:self.cursorIndex] + char + self.textMessage[self.cursorIndex:]
                self.cursorIndex+=1
                self.maxCurrentIndex += 1
                self.changeText()

    def moveCursorLeft(self):
        if self.cursorIndex > 0:
            self.cursorIndex -= 1
        if self.cursorIndex <= self.currentIndex:
            if self.cursorIndex > 0:
                self.cursorIndex+=1
                self.currentIndex-=1
                self.maxCurrentIndex-=1
            self.tempText = self.text.render(self.textMessage[self.currentIndex:self.maxCurrentIndex], False, self.textcolor)
            self.changeText()
        self.changeText()

    def updateCursor(self):
        if self.active:
            if self.mode == "scroll":
                if self.cursorIndex < 0:
                    self.cursorIndex = 0
                if self.cursorIndex > len(self.textMessage):
                    self.cursorIndex = len(self.textMessage)
                self.cursorTextObject = self.text.render(self.textMessage[self.currentIndex:self.cursorIndex], False, self.cursorColor)
                pygame.draw.rect(self.window,self.cursorColor,(self.x+self.cursorTextObject.get_width(),self.y,2,self.size))
            elif self.mode == "password":
                if self.cursorIndex < 0:
                    self.cursorIndex = 0
                if self.cursorIndex > len(self.textMessage):
                    self.cursorIndex = len(self.textMessage)
                self.cursorTextObject = self.text.render(len(self.textMessage[self.currentIndex:self.cursorIndex])*"*", False, self.cursorColor)
                pygame.draw.rect(self.window,self.cursorColor,(self.x+self.cursorTextObject.get_width(),self.y,2,self.size))
    
    def delChar(self):
        if self.cursorIndex > 0:
            self.textMessage = self.textMessage[:self.cursorIndex-1] + self.textMessage[self.cursorIndex:]
            self.cursorIndex-=1
        while self.textObject.get_width() < self.width - 5:
                self.currentIndex-=1
                
                self.textObject = self.text.render(self.textMessage[self.currentIndex:], False, self.textcolor)
                if self.currentIndex <= 0:
                    self.currentIndex=0
                    break
        if self.cursorIndex == 0:
                self.backLine()
        self.changeText()
    
    def backspace(self):
        self.backspacecounter += 0.1*self.backspacevelocity
        if self.backspacecounter > 1:
            self.backspacecounter = 0
            self.backspacevelocity += 0.5
            self.delChar()
    
    def letter(self,char):
        keys = pygame.key.get_pressed()
        self.lettercounter[char] += 0.05*self.lettervelocity[char]
        if self.lettercounter[char] > 1:
            self.lettercounter[char] = 0
            self.lettervelocity[char] += 0.5
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                self.addChar(char.upper())
            else:
                self.addChar(char)

    def left(self):
        self.leftarrowcount += 0.07*self.leftarrowvelocity
        if self.leftarrowcount > 1:
            self.leftarrowcount = 0
            self.leftarrowvelocity += 0.5
            self.moveCursorLeft()
    
    def right(self):
        self.rightarrowcount += 0.07*self.rightarrowvecolicty
        if self.rightarrowcount > 1:
            self.rightarrowcount = 0
            self.rightarrowvecolicty += 0.5
            
            self.addChar("")

    def backLine(self):
        if len(self.textList) > 0:
            print('yes', len(self.textList), self.textMessageList)
            self.textMessage = self.textMessageList[-1]
            del self.textList[-1]
            del self.textMessageList[-1]
            self.linecount -= 1
            self.fullMSG = self.fullMSG[:len(self.fullMSG)-len(self.textMessage)]
            self.y += 30
            self.cursorIndex = len(self.textMessage)
            self.changeText()
        

    def getStr(self):
        print()
        return self.fullMSG+self.textMessage


class Image:
    def __init__(self,filepath,x,y,width,height,window,pixelratio):
        self.filepath = filepath
        self.x = x/pixelratio
        self.y = y/pixelratio
        self.width = width/pixelratio
        self.height = height/pixelratio
        self.window = window
        self.image = pygame.image.load(self.filepath)
        self.image = pygame.transform.scale(self.image, (int(self.width),int(self.height)))
    
    def draw(self):
        self.window.blit(self.image,(self.x,self.y))

class Text:
    def __init__(self,font,color,message,window,x,y,pixelratio, size):
        self.font = font
        self.color=color
        self.window = window
        self.message=message
        self.pixel = pixelratio
        self.size=size//self.pixel
        self.newText = pygame.font.SysFont(font, int(self.size))
        self.textObject = self.newText.render(self.message, False, self.color)
        self.x=x/self.pixel-(self.textObject.get_width()/2)
        self.y=y/self.pixel-(self.textObject.get_height()/2)
        
    
    def draw(self):
        self.window.blit(self.textObject,(self.x,self.y))
    
    def changeText(self, newMessage):
        self.newText = pygame.font.SysFont(self.font, int(self.size))
        self.textObject = self.newText.render(newMessage, False, self.color)
        self.message = newMessage
    
class messageObject:
    def __init__(self,x,y,width,color,window,pixelratio,username,text,size, bordercolor):
        self.x=x/pixelratio
        self.width=width/pixelratio
        self.color=color
        self.window=window
        self.indepenty=size*2
        self.username=username
        self.text=text
        self.size = size/pixelratio
        self.bordercolor = bordercolor
        self.font = pygame.font.SysFont("Orbitron", int(self.size))
        self.newfont = pygame.font.SysFont("Orbitron", 2)
        self.messages = [self.font.render(" "+self.username, False, (2,217,168))]
        self.load_message()
        self.height = 64/pixelratio+(35/pixelratio*(len(self.messages)-2))
        self.relativey = self.height
        self.y=y/pixelratio
        self.linecount = len(self.messages)
        self.visible = True

    def draw(self):
        pygame.draw.rect(self.window,self.bordercolor,(self.x,self.y-self.indepenty,self.width,self.height),2,2)
        for i in range(len(self.messages)):
            self.window.blit(self.messages[i],(self.x,self.y+(i*self.size)-self.indepenty+5))

    def load_message(self):
        tempMessage = " "
        for i in range(len(self.text)):
            tempMessage += self.text[i]
            self.textObject = self.font.render(tempMessage, False, (255,255,255))
            if self.textObject.get_width() > self.width-20:
                self.messages.append(self.textObject)
                tempMessage = " "
        self.messages.append(self.font.render(tempMessage, False, (255,255,255)))

    def ChangeVis(self, newThing):
        self.visible = newThing

    def isActive(self):
        if self.visible:
            return True
        return False

class Placeholder:
    def __init__(self,y):
        self.y = y

class User:
    def __init__(self, name, window):
        self.window = window
        self.image = pygame.image.load("Images\person_outline.png")
        self.y = 250
        self.image = pygame.transform.scale(self.image, (100,100))
        self.name = name
        self.font = pygame.font.SysFont("Orbitron", 30)
        self.textObject = self.font.render(self.name, False, (193,146,252))

    def draw(self):
        self.window.blit(self.textObject,(160,self.y+50-15))
        self.window.blit(self.image, (50,self.y))