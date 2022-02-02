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
    def __init__(self,x,y,width,height,color,window,pixelratio,command,textcolor,mode,emptyMessage=""):
        self.x=x/pixelratio
        self.y=y/pixelratio
        self.width=width/pixelratio
        self.height=height/pixelratio
        self.color=color
        self.window=window
        self.command = command
        self.textcolor = textcolor
        self.emptyMessage=emptyMessage
        self.textMessage = emptyMessage
        self.tempMessage = ""
        self.mode = mode
        self.currentIndex = 0
        self.changeText()
    
    def draw(self):
        pygame.draw.rect(self.window,self.color,(self.x,self.y,self.width,self.height))
        self.window.blit(self.textObject,(self.x,self.y+(self.textObject.get_height()//2)))
    
    def click(self,mx,my):
        if self.x <= mx <= self.x+self.width and self.y <= my <= self.y+self.height:
            return True
        return 
    
    def changeText(self):
        if self.mode == "scroll":
            self.newText = pygame.font.SysFont("Orbitron", int(self.height))
            self.textObject = self.newText.render(self.textMessage[self.currentIndex:], False, self.textcolor)
            while self.textObject.get_width() > self.width - 5:
                self.currentIndex+=1
                self.newText = pygame.font.SysFont("Orbitron", int(self.height))
                self.textObject = self.newText.render(self.textMessage[self.currentIndex:], False, self.textcolor)
        

    def activate(self):
        if self.textMessage == self.emptyMessage:
            self.textMessage = ""
        self.changeText()
    
    def deactivate(self):
        if self.textMessage == "":
            self.textMessage = self.emptyMessage
        self.changeText()

    def addChar(self,char):
        self.textMessage += char

        self.changeText()
        
    
    def delChar(self):
        self.textMessage = self.textMessage[:-1]
        while self.textObject.get_width() < self.width - 5:
                self.currentIndex-=1
                self.newText = pygame.font.SysFont("Orbitron", int(self.height))
                self.textObject = self.newText.render(self.textMessage[self.currentIndex:], False, self.textcolor)
                if self.currentIndex <= 0:
                    self.currentIndex=0
                    break
        self.changeText()

class Image:
    def __init__(self,filepath,x,y,width,height,window,pixelratio):
        self.filepath = filepath
        self.x = x/pixelratio
        self.y = y/pixelratio
        self.width = width/pixelratio
        self.height = height/pixelratio
        self.window = window
        self.image = pygame.image.load(self.filepath)
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
    
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

    
    
