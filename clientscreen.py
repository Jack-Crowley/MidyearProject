import pygame
from chatroomManager import Chatroom
from loginscreen import Login

window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

MWIDTH, MHEIGHT = window.get_size()
pixelratio = 1920/MWIDTH

pygame.font.init()

Login(window,clock,pixelratio)
Chatroom(window,clock,pixelratio)
pygame.display.quit()