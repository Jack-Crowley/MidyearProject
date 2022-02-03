import pygame
from shapes import *
from chatroom_chatroomsscreen import chatroomsscreen
from chatroom_chatscreen import chatscreen
from chatroom_settingscreen import settingscreen



class Chatroom:
    def __init__(self, window,clock,pixelratio):
        self.window = window
        self.clock = clock
        self.pixelratio = pixelratio

        self.chatroomscreen = chatroomsscreen(self.window,self.pixelratio)
        self.chatscreen = chatscreen(self.window,self.pixelratio)
        self.settingscreen = settingscreen(self.window,self.pixelratio)

        self.active = chatscreen
        self.run = True

        while self.run:
            self.clock.tick(60)
            