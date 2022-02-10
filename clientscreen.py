import pygame
from chatroomManager import Chatroom
from loginscreen import Login
from registerscreen import Register
from client import Client

window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

validUsernames = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
validChars = "`123f4567890-=~!@#$% ^&*v()_+qwertyuiop[]\\asdghjxkl'zcbn,./ZXCVBNM<>?ASDFGHJKL:;\"QWERTYUIOP{}|m"


MWIDTH, MHEIGHT = window.get_size()
pixelratio = 1920/MWIDTH

pygame.font.init()

login = Login(window,clock,pixelratio,validUsernames)
#register = Register(window,clock,pixelratio,validChars)
username = login.username.textMessage
password = login.password.textMessage

client = Client(username,password)

Chatroom(window,clock,pixelratio,validChars, client)
pygame.display.quit()