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
        print(self.textObject.get_height())
        
    
    def draw(self):
        self.window.blit(self.textObject,(self.x,self.y))
    
    



class Login:
    def __init__(self,window):
        pygame.font.init()

        self.window = window

        self.MWIDTH, self.MHEIGHT = self.window.get_size()
        self.pixelratio = 1920/self.MWIDTH

        self.drawables=[]
        self.loadDrawables()

        self.run = True
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.run = False
            
            self.draw()
        
    def loadDrawables(self):
        self.drawables.append(Rectangle(0,0,1920,192,(17,17,17),self.window,self.pixelratio))
        self.drawables.append(Rectangle(576,300,768,700,(17,17,17),self.window,self.pixelratio))
        self.drawables.append(Text("Orbitron",(193,146,252),"PERMEABILITY",self.window,960,96,self.pixelratio,192))


    def draw(self):
        self.window.fill((27,27,27))
        for i in self.drawables:
            i.draw()
        pygame.display.update()