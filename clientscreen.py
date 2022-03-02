import pygame
from chatroomManager import Chatroom
from loginscreen import Login
from registerscreen import Register
from client import Client


window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

validUsernames = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '
validChars = "`123f4567890-=~!@#$% ^&*v()_+qwertyuiop[]\\asdghjxkl'zcbn,./ZXCVBNM<>?ASDFGHJKL:;\"QWERTYUIOP{}|m"


MWIDTH, MHEIGHT = window.get_size()
pixelratio = 1920/MWIDTH

pygame.font.init()

with open('nothing.txt') as data: nstring = data.read().strip()

login = Login(window,clock,pixelratio,validUsernames)
while login.newScreen != None:
    if login.newScreen == "register":
        register = Register(window,clock,pixelratio,validUsernames)
    login = Login(window,clock,pixelratio,validUsernames)
username = login.username.textMessage
password = login.password.textMessage

client = Client(username,password)
print('connected')

Chatroom(window,clock,pixelratio,validChars,client, username)
pygame.display.quit()