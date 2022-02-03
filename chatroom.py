import pygame

class Chatroom:
    def __init__(self, window):
        self.window = window

        self.run = True
        
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.run = False
            window.fill((0,255,255))
            pygame.display.update()
