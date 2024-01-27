import pygame as pg
import os
from settings import *

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.stop()
        pg.mixer.init()
        self.path = SOUND_PATH

        pg.mixer.set_num_channels(CH_MAX)  # default is 8
        self.CH_PLY = pg.mixer.Channel(0)    # player sounds
        self.CH_WPN = pg.mixer.Channel(1)    # player weapons
        self.CH_NPC = pg.mixer.Channel(2)    # npc
        self.CH_NPC_W = pg.mixer.Channel(3)  # npc weapons
        self.CH_AMB = pg.mixer.Channel(4)    # ambient sounds (doors...)
        self.CH_MUS = pg.mixer.Channel(5)    # music

        #self.play_soundtrack(self.game.map.soundtrack)

    def play_soundtrack(self):
        try:
            self.CH_MUS.play(pg.mixer.Sound(SOUND_PATH + 'soundtrack/' + self.game.map.soundtrack))
        except:
            return
