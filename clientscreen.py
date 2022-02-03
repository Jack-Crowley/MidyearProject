import pygame
from chatroom import Chatroom
from loginscreen import Login

window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

pygame.font.init()

Login(window,clock)
Chatroom(window)
pygame.display.quit()