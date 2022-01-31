import pygame


class Login:
    def __init__(self,window):
        window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    run = False
            window.fill((255,0,0))
            pygame.display.update()