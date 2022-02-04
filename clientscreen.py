import pygame
from chatroomManager import Chatroom
from loginscreen import Login

window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

validChars = "`123f4567890-=~!@#$% ^&*v()_+qwertyuiop[]\\asdghjxkl'zcbn,./ZXCVBNM<>?ASDFGHJKL:;\"QWERTYUIOP{}|m"


MWIDTH, MHEIGHT = window.get_size()
pixelratio = 1920/MWIDTH

pygame.font.init()

Login(window,clock,pixelratio,validChars)
Chatroom(window,clock,pixelratio,validChars)
pygame.display.quit()