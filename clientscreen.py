import pygame
from chatroom import Chatroom
from loginscreen import Login

window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

Login(window)
Chatroom(window)


pygame.display.quit()