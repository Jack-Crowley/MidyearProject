import pygame


class Login:
    def __init__(self,window):
        window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

        self.run = True

        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.run = False
            window.fill((255,0,0))
            pygame.display.update()